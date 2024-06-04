from rest_framework import generics, status
from .models import CurrencyRate
from .serializers import CurrencyRateSerializer
from rest_framework.response import Response
import requests
from datetime import datetime, timedelta
from django.db.models import Count

class CurrencyRateList(generics.ListCreateAPIView):
    def split_date_range(self, start_date, end_date, max_days=93):
        ranges = []
        current_start = start_date
        current_end = min(start_date + timedelta(days=92), end_date)
        while current_start <= end_date:
            ranges.append((current_start, current_end))
            current_start += timedelta(days=max_days)
            current_end = min(current_start + timedelta(days=92), end_date)
        return ranges
    
    def get(self, request, *args, **kwargs):
        
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Validate date format
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use Y-m-d.'}, status=status.HTTP_400_BAD_REQUEST)

        date_ranges = self.split_date_range(start_date_obj, end_date_obj)

        existing_dates = set(CurrencyRate.objects.values_list('date', flat=True))

        for start, end in date_ranges:
            url = f'http://api.nbp.pl/api/exchangerates/tables/A/{start}/{end}/?format=json'
            response = requests.get(url)

            if response.status_code != 200:
                return Response({'error': 'Failed to fetch data from NBP API.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            data = response.json()
            rates = []

            for table in data:
                effective_date = datetime.strptime(table['effectiveDate'], '%Y-%m-%d').date()
                
                for rate in table['rates']:
                    currency_rate = {
                        'currency_symbol': rate['code'],
                        'rate': rate['mid'],
                        'date': table['effectiveDate']
                    }
                    rates.append(currency_rate)

                    if effective_date in existing_dates:
                        continue

                    CurrencyRate.objects.create(
                        currency_symbol=rate['code'],
                        rate=rate['mid'],
                        date=table['effectiveDate']
                    )

        serializer = CurrencyRateSerializer(data=rates, many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)