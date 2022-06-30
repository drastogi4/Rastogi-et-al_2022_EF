load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
begin
;This script calculates pattern correlation, bias and ratio of standard deviation at seasonal scale

;Variables
var      = (/"tmax","tmin","prcp"/)

;CMIP6 models
model    = (/"ACCESS-CM2","BCC-CSM2-MR","CNRM-ESM2-1","MPI-ESM1-2-HR","MRI-ESM2-0","NorESM2-MM"/)

;Experiments
sim      = (/"CMIP6","RegCM","Livneh_RegCM","Daymet_RegCM","Livneh_DBCCA","Daymet_DBCCA"/)

;Number of latitude and longitude
nlat     = 697
nlon     = 1405

;Looping over experiments
do ss    = 0,dimsizes(sim)-1

re_D     = new((/dimsizes(model),dimsizes(var),4,3/),"float")
re_L     = new((/dimsizes(model),dimsizes(var),4,3/),"float")
pc_D     = new((/dimsizes(model),dimsizes(var),4,3/),"float")
pc_L     = new((/dimsizes(model),dimsizes(var),4,3/),"float")

;Looping over variables
do vv    = 0,dimsizes(var)-1

vardiff  = new((/4,nlat,nlon/),"float")
var_Daymet  = new((/4,nlat,nlon/),"float")
var_Livneh  = new((/4,nlat,nlon/),"float")


inputvar  = var(vv)

;Reading reference data
fD = addfile("./netcdf/Daymet_1980-2019_"+var(vv)+"_monmean.nc","r")
fL = addfile("./netcdf/Livneh_1980-2018_"+var(vv)+"_monmean.nc","r")

var_Daymet1 = fD->$var(vv)$(0:38,:,:,:)
var_Livneh1 = fL->$var(vv)$(0:38,:,:,:)
var_Daymet2 = dim_avg_n_Wrap(var_Daymet1,0)
var_Livneh2 = dim_avg_n_Wrap(var_Livneh1,0)

;Calculate seasonal averages
var_Daymet(0,:,:) = (var_Daymet2(11,:,:)+var_Daymet2(0,:,:)+var_Daymet2(1,:,:))/3
var_Daymet(1,:,:) = dim_avg_n_Wrap(var_Daymet2(2:4,:,:),0)
var_Daymet(2,:,:) = dim_avg_n_Wrap(var_Daymet2(5:7,:,:),0)
var_Daymet(3,:,:) = dim_avg_n_Wrap(var_Daymet2(8:10,:,:),0)

var_Livneh(0,:,:) = (var_Livneh2(11,:,:)+var_Livneh2(0,:,:)+var_Livneh2(1,:,:))/3
var_Livneh(1,:,:) = dim_avg_n_Wrap(var_Livneh2(2:4,:,:),0)
var_Livneh(2,:,:) = dim_avg_n_Wrap(var_Livneh2(5:7,:,:),0)
var_Livneh(3,:,:) = dim_avg_n_Wrap(var_Livneh2(8:10,:,:),0)

;Looping over the models
do mm     = 0,dimsizes(model)-1

;Reading data for experiments
f1   = addfile("./netcdf/"+model(mm)+"_"+sim(ss)+"_1980-2059_"+inputvar+"_monmean.nc","r")

vartmp            = f1->$inputvar$(0:38,:,:,:)
vardiff1   = dim_avg_n_Wrap(vartmp(:,:,:,:),0)

;Calculate seasonal averages
vardiff(0,:,:) = (vardiff1(11,:,:)+vardiff1(0,:,:)+vardiff1(1,:,:))/3
vardiff(1,:,:) = dim_avg_n_Wrap(vardiff1(2:4,:,:),0)
vardiff(2,:,:) = dim_avg_n_Wrap(vardiff1(5:7,:,:),0)
vardiff(3,:,:) = dim_avg_n_Wrap(vardiff1(8:10,:,:),0)


do seas = 0,3
re_D(mm,vv,seas,0)  = pattern_cor(vardiff(seas,:,:),var_Daymet(seas,:,:),1.0,0)
re_D(mm,vv,seas,1)  = stddev(vardiff(seas,:,:))/stddev(var_Daymet(seas,:,:))
re_D(mm,vv,seas,2)  = avg(vardiff(seas,:,:)-var_Daymet(seas,:,:))
re_L(mm,vv,seas,0)  = pattern_cor(vardiff(seas,:,:),var_Livneh(seas,:,:),1.0,0)
re_L(mm,vv,seas,1)  = stddev(vardiff(seas,:,:))/stddev(var_Livneh(seas,:,:))
re_L(mm,vv,seas,2)  = avg(vardiff(seas,:,:)-var_Livneh(seas,:,:))
end do

end do

re_D!1      = "variables"
re_D!2      = "season"
re_D!3      = "stats"
re_D!0      = "model"
re_L!1      = "variables"
re_L!2      = "season"
re_L!3      = "stats"
re_L!0      = "model"

;Write the output in a netcdf file
system("rm PatternCorrelation_RatioSD_Bias_Livneh_"+sim(ss)+".nc")
fout1        = addfile("PatternCorrelation_RatioSD_Bias_Livneh_"+sim(ss)+".nc","c")
fout1->re    = re_L

system("rm PatternCorrelation_RatioSD_Bias_Daymet_"+sim(ss)+".nc")
fout1        = addfile("PatternCorrelation_RatioSD_Bias_Daymet_"+sim(ss)+".nc","c")
fout2->re    = re_D


end
