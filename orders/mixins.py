from django.utils.dateparse import parse_date
from django.contrib import messages
from datetime import date

class OrderFilterMixin: #Mixin per applicare filtri agli ordini, sia per la pagina utente che per la pagina manager
    def apply_filters(self, orders):
        status = self.request.GET.get("status")
        if status:
            if(status != "Tutti"):
                orders = orders.filter(status=status)
        order_id = self.request.GET.get("id")
        if order_id:
            orders = orders.filter(id=order_id)
        start_date = self.request.GET.get("start_date")
        if start_date:
            parsed = parse_date(start_date) #controllo sul formato della data
            if parsed is None:
                messages.error(self.request, "Formato data di inizio non valido. Utilizzare il formato DD-MM-YYYY.")
            elif parsed > date.today():
                messages.error(self.request, "La data di inizio non può essere nel futuro.")
            else:
                orders = orders.filter(created_at__date__gte=parsed)
        end_date = self.request.GET.get("end_date")
        if end_date:
            parsed = parse_date(end_date) #controllo sul formato della data
            if parsed is None:
                messages.error(self.request, "Formato data di fine non valido. Utilizzare il formato DD-MM-YYYY.")
            elif parsed > date.today():
                messages.error(self.request, "La data di fine non può essere nel futuro.")
            else:
                orders = orders.filter(created_at__date__lte=parsed)
            
        return orders