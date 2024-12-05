from .models import *
from .serializers import *
# Slick Reporting
from django.db.models import Sum, Count, Avg, Max, Min
from slick_reporting.views import ReportView, Chart
from slick_reporting.fields import ComputationField

# Reports By Slick Reporting


class CountValueComputationField(ComputationField):
    calculation_method = Count
    calculation_field = "id"
    verbose_name = "Count"
    name = "count_value"


class ServiceReport(ReportView):
    report_model = Service
    date_field = "created_at"
    group_by = "state"
    columns = [
        "state", CountValueComputationField,
    ]

    chart_settings = [
        Chart(
            "Services By State [BAR Chart]",
            Chart.BAR,
            data_source=["count_value"],
            title_source=["state"],
        ),
        Chart(
            "Services By State [PIE Chart]",
            Chart.PIE,
            data_source=["count_value"],
            title_source=["state"],
        ),
    ]


class ServiceByTechReport(ReportView):
    report_model = Service
    date_field = "created_at"
    group_by = "worker__first_name"

    columns = [
        "worker__first_name",
        ComputationField.create(
            Count, "id", name="count", verbose_name="Tech Services"
        ),
        ComputationField.create(
            Avg, "feedback__rate", name="avg", verbose_name="Average Rate", is_summable=False
        )
    ]
    chart_settings = [
        Chart(
            "Services Count By Tech [BAR Chart]",
            Chart.BAR,
            data_source=["count"],
            title_source=["worker__first_name"],
        ),
        Chart(
            "Tech Average Rating[BAR Chart]",
            Chart.BAR,
            data_source=["avg"],
            title_source=["worker__first_name"],
        ),
        Chart(
            "Services Count By Tech [PIE Chart]",
            Chart.PIE,
            data_source=["count"],
            title_source=["worker__first_name"],
        ),

    ]


class DeviceReport(ReportView):
    report_model = Device
    date_field = "created_at"
    group_by = "device_type"
    columns = [
        "name", CountValueComputationField,
    ]

    chart_settings = [
        Chart(
            "Devices By Type [BAR Chart]",
            Chart.BAR,
            data_source=["count_value"],
            title_source=["name"],
        ),
        Chart(
            "Devices By Type [PIE Chart]",
            Chart.PIE,
            data_source=["count_value"],
            title_source=["name"],
        ),
    ]


class FeedbackReport(ReportView):
    report_model = Feedback
    date_field = "created_at"
    group_by = "rate"
    columns = [
        "rate",
        ComputationField.create(
            Count, "id", name="count__value", verbose_name="Count", is_summable=False
        ),
    ]

    chart_settings = [
        Chart(
            "Feedbacks By Rate [BAR Chart]",
            Chart.BAR,
            data_source=["count__value"],
            title_source=["rate"],
        ),
        Chart(
            "Feedbacks By Rate [PIE Chart]",
            Chart.PIE,
            data_source=["count__value"],
            title_source=["rate"],
        ),
    ]
