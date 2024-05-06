# Home Assistant Tuya IR Air Conditioner Integration

![Example Image](https://github.com/DavidIlie/tuya-smart-ir-ac/assets/47594764/c91995e3-474c-47df-83f6-eaf64371a1d4)

> **WARNING:** This is by no means a custom component which I can assure works with everything, this is tailored to my needs as part of my initial project which you can find [here](https://davidilie.com) but I hope to work on making it more broad and also a standard repository with a good dev environment. Maybe someone can help me out here.

# It's fork for tuya us datacenter

The copyright to this fork belongs to DavidIllie

## Adding it to Home Assistant

I don't know how to create a UI (SOMETHING TODO) so here is the basic configuration for HA:

```yaml
climate:
   - platform: tuya_smart_ir_ac
     name: "Thermostat"
     sensor: "sensor.whatever_sensor_you_have"
     access_id: ""
     access_secret: ""
     remote_id: ""       # smart ir id
     ac_id: ""        # ac id
```
![image](https://github.com/plplaaa2/tuya-smart-ir-ac/assets/124797654/04bbf3fe-1e49-4e24-9e18-1d561eb374d5)

![image](https://github.com/plplaaa2/tuya-smart-ir-ac/assets/124797654/1f60454b-e83f-4812-a55d-d51acf08057a)


**You can find the IDs from the Tuya Iot Website!**
