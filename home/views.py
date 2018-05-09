from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer, CustomerSerializer, CircuitSerializer, SiteSerializer
from home.models import Circuit, Customer, Site
import csv
import io
import re
from collections import OrderedDict, defaultdict

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=self.request.FILES)

        if file_serializer.is_valid():
            try:
                csv_file = request.FILES["file"]
                if not csv_file.name.endswith('.csv'):
                    return Response('File is not CSV type')
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                io_string.readline()
                for line in csv.reader(io_string, delimiter=';', quotechar='|'):
                    line = line[0].split(',')
                    mep_id = line[0]
                    cir_az = line[1]
                    cir_za = line[2]
                    customer_name = line[3]
                    circuit_id  = line[4]
                    a_hw_version = line[5]
                    z_hw_version = line[6]
                    state = line[7]
                    city = line[8]
                    address = line[9]
                    a_ip = line[10]
                    z_ip = line[11]
                    pat = re.match(r"^\d{1,2}.[A-Z]{1}\d{1}[A-Z]{2}.\d{1,4}.[A-Z]{4}", circuit_id)
                    if a_ip != z_ip and pat:                       
                        customer = Customer(customer_name=customer_name, state=state, city=city, address=address)
                        customer.save()
                        circuit = Circuit(customer=customer, circuit_id=circuit_id, mep_id=mep_id, cir_az=cir_az, cir_za=cir_za)
                        circuit.save()
                        site = Site(circuit=circuit, ip=a_ip, hw_version=a_hw_version,type='A')
                        site.save()
                        site = Site(circuit=circuit, ip=z_ip, hw_version=z_hw_version, type='Z')
                        site.save()
                data = {'status': 'Data uploaded successfully.'}
                return Response(data)
            except Exception as e:
                return Response(e)            
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def to_dict(data):
    d = OrderedDict()
    d['MEP_ID'] = data[0]['circuit']['mep_id']
    d['CIR_AZ'] = data[0]['circuit']['cir_az']
    d['CIR_ZA']  = data[0]['circuit']['cir_za']
    d['CUSTOMER']  = data[0]['circuit']['customer']['customer_name']
    d['CIRCUITID'] = data[0]['circuit']['circuit_id']
    d['A_HW_VERSION'] = data[0]['hw_version']
    d['Z_HW_VERSION'] = data[1]['hw_version'] 
    d['STATE']  = data[0]['circuit']['customer']['state']
    d['CITY']  = data[0]['circuit']['customer']['city']
    d['ADDRESS']  = data[0]['circuit']['customer']['address']
    d['A_IP']  = data[0]['ip']
    d['Z_IP']= data[1]['ip']              
    return d


class GetCircuit(APIView):

    def get(self, request, *args, **kwargs):   
        try:     
            circuitid = self.request.query_params.get('name')       
            circuit = Circuit.objects.get(circuit_id=circuitid)        
            sites = Site.objects.filter(circuit=circuit)
            serializer = SiteSerializer(sites, many=True)
            data = serializer.data
            return Response(to_dict(data))
        except Exception as e:
            return Response(e)
        


class GetCircuits(APIView):

    def get(self, request, *args, **kwargs):  
        try:              
            customer_name = self.request.query_params.get('name') 
            customer = Customer.objects.filter(customer_name=customer_name)       
            circuits = Circuit.objects.filter(customer__in=customer)
            data_list = []
            for circuit in circuits:
                sites = Site.objects.filter(circuit=circuit)
                serializer = SiteSerializer(sites, many=True)
                data = serializer.data            
                data_list.append(to_dict(data))        
            return Response(data_list)
        except Exception as e:
            return Response(e)
        


 
