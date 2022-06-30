load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
begin
;This script calculates pattern correlation, bias and ratio of standard deviation at annual scale

;indices
var      = (/"tmax","tmin","prcp","t95","t05","p95","wetdays","frostdays"/)

;CMIP6 models
model    = (/"ACCESS-CM2","BCC-CSM2-MR","CNRM-ESM2-1","MPI-ESM1-2-HR","MRI-ESM2-0","NorESM2-MM"/)

;Experiments
sim      = (/"CMIP6","RegCM","Livneh_RegCM","Daymet_RegCM","Livneh_DBCCA","Daymet_DBCCA"/)
nlat     = 697
nlon     = 1405

;Looping over experiments
do ss    = 0,dimsizes(sim)-1

re_D     = new((/dimsizes(model),dimsizes(var),3/),"float")
re_L     = new((/dimsizes(model),dimsizes(var),3/),"float")

;Looping over indices
do vv    = 0,dimsizes(var)-1
var_Daymet  = new((/nlat,nlon/),"float")
var_Livneh  = new((/nlat,nlon/),"float")


;Reading reference data
if(var(vv).eq."p95".or.var(vv).eq."t95".or.var(vv).eq."t05") then
fD = addfile("./netcdf/Daymet_1980-2018_"+var(vv)+".nc","r")
fL = addfile("./netcdf/Livneh_1980-2018_"+var(vv)+".nc","r")
else
fD = addfile("./netcdf/Daymet_1980-2019_"+var(vv)+".nc","r")
fL = addfile("./netcdf/Livneh_1980-2018_"+var(vv)+".nc","r")
end if

var_Daymet1 = fD->$var(vv)$(0:38,:,:)
var_Livneh1 = fL->$var(vv)$(0:38,:,:)
var_Daymet = dim_avg_n_Wrap(var_Daymet1,0)
var_Livneh = dim_avg_n_Wrap(var_Livneh1,0)

;Looping over the models
do mm     = 0,dimsizes(model)-1

;Reading data for experiments
if(var(vv).eq."p95".or.var(vv).eq."t95".or.var(vv).eq."t05") then
f1                = addfile("./netcdf/"+model(mm)+"_"+sim(ss)+"_1980-2018_"+inputvar+".nc","r")
else
f1                = addfile("./netcdf/"+model(mm)+"_"+sim(ss)+"_1980-2059_"+inputvar+".nc","r")
end if

vartmp            = f1->$inputvar$(0:38,:,:)
vardiff           = dim_avg_n_Wrap(vartmp(:,:,:),0)

;Calculate statistics
re_D(mm,vv,0)   = pattern_cor(vardiff,var_Daymet,1.0,0)
re_D(mm,vv,1)   = stddev(vardiff)/stddev(var_Daymet)
re_D(mm,vv,2)   = avg(vardiff-var_Daymet)
re_L(mm,vv,0)   = pattern_cor(vardiff,var_Livneh,1.0,0)
re_L(mm,vv,1)   = stddev(vardiff)/stddev(var_Livneh)
re_L(mm,vv,2)   = avg(vardiff-var_Livneh)

end do

re_D!2     = "stats"
re_D!1      = "variables"
re_D!0      = "model"
re_L!2      = "stats"
re_L!1      = "variables"
re_L!0      = "model"
end do
end do
end
