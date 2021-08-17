"""
Therapistfinder - therapistfinder/util/time.py

Author/s: olel
Therapistfinder (thus this code) is public domain.
"""

def filter_current_timeslots(current_hour, current_minute, slots):
    current_time = (100 * current_hour + current_minute)
    result = []
    for slot in slots:
        slot_start = (slot.start_hour * 100 + slot.start_minute)
        slot_end = (slot.end_hour * 100 + slot.end_minute)
        if current_time >= slot_start and current_time < slot_end:
            result.append(slot)
    return result