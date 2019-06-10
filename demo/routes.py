def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('invoice','/invoice/{action}')
    config.add_route('invoices','/invoices/')
    config.add_route('item','/item/{action}')
