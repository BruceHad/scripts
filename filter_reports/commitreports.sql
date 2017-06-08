-- This will list all locations still set to receive paper reports
select
  loc.location_no
from dpdapp.list_numbers ln
  inner join dpdapp.list_number_locations lnl
  on (ln.list_number = lnl.ln_list_number)
  inner join dpdapp.locations loc
  on (loc.location_no = lnl.loc_location_no)
where 1=1
  and ln.gdpa_designated = 'Y'
  and ln.commence_date <= sysdate
  and (ln.resign_date is null or ln.resign_date > sysdate)  
  and ln.report_destination in ('P', 'B')
--  and loc.location_no = 5307
order by location_no
;