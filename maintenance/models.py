from django.db import models
from engine_room.models import PortEngine, \
    PortEngine2, PortEngine3, StarboardEngine, StarboardEngine2, StarboardEngine3, \
    CenterEngine, Auxiliary, GenSet, GenSet2, MainEngine
# Create your models here.


class ServiceSchedule(models.Model):
    # Related Odometer
    odometer_center = models.ForeignKey(CenterEngine, on_delete=models.SET_NULL, null=True, blank=True)
    odometer_main = models.ForeignKey(MainEngine, on_delete=models.SET_NULL, null=True, blank=True)
    odometer_port = models.ForeignKey(PortEngine, on_delete=models.SET_NULL, null=True, blank=True)
    odometer_port2 = models.ForeignKey(PortEngine2, on_delete=models.SET_NULL, null=True, blank=True)
    odometer_port3 = models.ForeignKey(PortEngine3, on_delete=models.SET_NULL, null=True, blank=True)
    odometer_starboard = models.ForeignKey(StarboardEngine, on_delete=models.SET_NULL, null=True, blank=True)
    odometer_starboard2 = models.ForeignKey(StarboardEngine2, on_delete=models.SET_NULL, null=True, blank=True)
    odometer_starboard3 = models.ForeignKey(StarboardEngine3, on_delete=models.SET_NULL, null=True, blank=True)
    odometer_auxiliary = models.ForeignKey(Auxiliary, on_delete=models.SET_NULL, null=True, blank=True)
    odometer_genset = models.ForeignKey(GenSet, on_delete=models.SET_NULL, null=True, blank=True)
    odometer_genset2 = models.ForeignKey(GenSet2, on_delete=models.SET_NULL, null=True, blank=True)

    # conditions
    repeated_short_trips_less_than_5_miles = models.BooleanField(default=False)
    repeated_short_trips_less_than_10_miles_outside_below_freezing = models.BooleanField(default=False)
    hot_weather_stop_and_go_traffic = models.BooleanField(default=False)
    extensive_idling_and_or_low_speed_driving_for_long_distances = models.BooleanField(default=False)
    driving_in_dusty_conditions = models.BooleanField(default=False)
    driving_on_rough_muddy_or_salt_spread_roads = models.BooleanField(default=False)
    towing_a_trailer_or_driving_with_a_car_top_carrier_installed = models.BooleanField(default=False)

    # engine
    engine_oil_miles = models.IntegerField(default=3750)
    engine_oil_months = models.PositiveIntegerField(default=3)
    engine_oil_filter_miles = models.PositiveIntegerField(default=3750)
    engine_oil_filter_months = models.PositiveIntegerField(default=3)
    air_cleaner_filter = models.PositiveIntegerField(default=30000)
    air_cleaner_months = models.PositiveIntegerField(default=24)
    vapor_lines_miles = models.PositiveIntegerField(default=30000,
                                                    help_text='inspect, correct or replace as necessary')
    vapor_lines_months = models.PositiveIntegerField(default=24)
    fuel_lines_miles = models.PositiveIntegerField(default=30000,
                                                   help_text='inspect, correct or replace as necessary')
    fuel_lines_months = models.PositiveIntegerField(default=24)
    fuel_filter_miles = models.PositiveIntegerField(default=210000,
                                                    help_text='inspect, correct or replace as necessary')
    fuel_filter_months = models.PositiveIntegerField(default=168)
    engine_coolant_miles = models.PositiveIntegerField(default=60000)
    engine_coolant_months = models.PositiveIntegerField(default=48)
    drive_belts_miles = models.PositiveIntegerField(default=30000)
    drive_belts_months = models.PositiveIntegerField(default=24)
    spark_plugs_miles = models.PositiveIntegerField(default=30000)
    spark_plugs_months = models.PositiveIntegerField(default=24)
    timing_belt_miles = models.PositiveIntegerField(default=105000)
    timing_belt_months = models.PositiveIntegerField(default=84)

    # brakes and differential
    brake_lines_and_cables = models.PositiveIntegerField(
        default=15000,
        help_text='inspect, correct or replace as necessary'
    )
    brake_lines_and_cables_months = models.PositiveIntegerField(default=12)

    brake_pads_disc_drums_and_linings = models.PositiveIntegerField(
        default=7500,
        help_text='inspect, correct or replace as necessary'
    )
    brake_pads_disc_drums_and_linings_months = models.PositiveIntegerField(default=6)

    four_wheel_drive_transfer_fluid_differential_gear_oil = models.PositiveIntegerField(
        default=15000,
        help_text='inspect, correct or replace as necessary'
    )
    four_wheel_drive_transfer_fluid_differential_gear_oil_months = models.PositiveIntegerField(default=12)

    limited_slip_differential_gear_oil = models.PositiveIntegerField(
        default=15000,
        help_text='inspect, correct or replace as necessary'
    )
    limited_slip_differential_gear_oil_months = models.PositiveIntegerField(default=12)

    exhaust_system = models.PositiveIntegerField(default=7500, help_text='inspect, correct or replace as necessary')
    exhaust_system_months = models.PositiveIntegerField(default=6)

    drive_shaft_boots_and_propeller_shaft = models.PositiveIntegerField(
        default=7500,
        help_text='inspect, correct or replace as necessary'
    )
    drive_shaft_boots_and_propeller_shaft_months = models.PositiveIntegerField(default=6)

    propeller_shaft_grease = models.PositiveIntegerField(
        default=7500,
        help_text='lubricate, inspect, correct or replace as necessary'
    )
    propeller_shaft_grease_months = models.PositiveIntegerField(default=6)

    steering_gear_and_suspension_parts = models.PositiveIntegerField(
        verbose_name='steering gear linkage, ball joints, axle, and suspension parts',
        default=7500,
        help_text='inspect, correct or replace as necessary'
    )
    steering_gear_and_suspension_parts_months = models.PositiveIntegerField(
        verbose_name='steering gear linkage, ball joints, axle, and suspension parts',
        default=6
    )

    front_wheel_bearing_grease = models.PositiveIntegerField(
        default=15000,
        help_text='inspect, correct or replace as necessary'
    )
    front_wheel_bearing_grease_months = models.PositiveIntegerField(default=12)

    supplemental_air_bag_system = models.PositiveIntegerField(default=500000)
    supplemental_air_bag_system_months = models.PositiveIntegerField(default=120)

    def __str__(self):
        return str(self.odometer_main)