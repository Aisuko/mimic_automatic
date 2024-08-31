-- Determines if a patient is ventilated on the first day of their ICU stay.
-- Creates a table with the result.
-- Requires the `ventilation_durations` table, generated by ../ventilation-durations.sql

select
  ie.subject_id, ie.hadm_id, ie.icustay_id
  -- if vd.icustay_id is not null, then they have a valid ventilation event
  -- in this case, we say they are ventilated
  -- otherwise, they are not
  , max(case
      when vd.icustay_id is not null then 1
    else 0 end) as vent
FROM `physionet-data.mimiciii_clinical.icustays` ie
left join `physionet-data.mimiciii_derived.ventilation_durations` vd
  on ie.icustay_id = vd.icustay_id
  and
  (
    -- ventilation duration overlaps with ICU admission -> vented on admission
    (vd.starttime <= ie.intime and vd.endtime >= ie.intime)
    -- ventilation started during the first day
    OR (vd.starttime >= ie.intime and vd.starttime <= DATETIME_ADD(ie.intime, INTERVAL '1' DAY))
  )
group by ie.subject_id, ie.hadm_id, ie.icustay_id
order by ie.subject_id, ie.hadm_id, ie.icustay_id;
