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
            orders = orders.filter(created_at__gte=start_date)
        end_date = self.request.GET.get("end_date")
        if end_date:
            orders = orders.filter(created_at__lte=end_date)
        
        return orders