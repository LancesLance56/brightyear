from src.create_app import create_app
from prometheus_flask_exporter import PrometheusMetrics

site=create_app()

metrics = PrometheusMetrics(site)

order_counter = metrics.counter(
    'plywood_inquiries_total', 'Number of Viber inquires',
    labels={'location': 'QuezonCity'}
    )

@site.route('/quezon-city-bright-year-plywood-contact')
def contact():
    order_counter.inc()
    return "Contact attempted!"
