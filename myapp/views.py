from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
purchase_mapping = ['consumerId', 'productId', 'productName', 'quantity',
                    'item_price', 'discount', 'tax', 'final_price']

mandatory_fields = ['consumerId', 'productId', 'productName', 'quantity', 'item_price']


@csrf_exempt
def purchases(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            mandatory_flag = True

            print(data)

            for field in mandatory_fields:
                if data.get(field) is None:
                    mandatory_flag = False

            if not mandatory_flag:
                return JsonResponse({"error": "Missing Mandatory fields"}, status=400)

            if not data.get('tax') or int(data.get('tax')) < 0:
                data['tax'] = 18

            if not data.get('discount') or int(data.get('discount')) < 0:
                data['discount'] = 0

            total_price = abs(int(data.get('quantity'))) * abs(int(data.get('item_price')))
            total_discounted_price = total_price - total_price * int(data.get('discount')) / 100
            total_taxed_price = total_discounted_price + int(data.get('tax')) * total_discounted_price / 100
            data['final_price'] = total_discounted_price

            # Process the purchase (dummy logic for now)
            response_data = {
                "consumerId": data["consumerId"],
                "product_id": data["productId"],
                "quantity": data["quantity"],
                "productName": data["productName"],
                "item_price": data["item_price"],
                "discount": data["discount"],
                "tax": data["tax"],
                "final_price": data["final_price"]
            }

            return JsonResponse({"message": "Received Successfully", "data": response_data}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
