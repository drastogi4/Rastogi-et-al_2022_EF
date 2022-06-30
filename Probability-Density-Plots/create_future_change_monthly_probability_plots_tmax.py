import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read monthly data from each experiment for the given variable
vv1 = "tmax"
fD = nc.Dataset(f'../analysis/netcdf/Daymet_1980-2019_{vv1}.nc')
fL = nc.Dataset(f'../analysis/netcdf/Livneh_1980-2018_{vv1}.nc')
f1 = nc.Dataset(f'../analysis/netcdf/CMIP6_1980-2059_{vv1}.nc')
f2 = nc.Dataset(f'../analysis/netcdf/RegCM_1980-2059_{vv1}.nc')
f3 = nc.Dataset(f'../analysis/netcdf/Livneh_RegCM_1980-2059_{vv1}.nc')
f4 = nc.Dataset(f'../analysis/netcdf/Daymet_RegCM_1980-2059_{vv1}.nc')
f5 = nc.Dataset(f'../analysis/netcdf/Livneh_DBCCA_1980-2059_{vv1}.nc')
f6 = nc.Dataset(f'../analysis/netcdf/Daymet_DBCCA_1980-2059_{vv1}.nc')

#Read data for the reference (1980-2019) and future (2020-2059) periods for each experiment
#Calculate historical climatology for each month and substract from each future year
#Create probability density plots for the futue change
varhis11  = f1.variables['pr'][0:40,:,:,:]
varssp1   = f1.variables['pr'][40:,:,:,:]
varhis111 = np.nanmean(varhis11, axis=0)
varhis1   = np.broadcast_to(varhis111,(40,12,697,1405))
vardiff1  = varssp1-varhis1 
sns.kdeplot(vardiff1.flatten(),color='dimgray')

varhis22  = f2.variables['prcp'][0:40,:,:,:]
varssp2   = f2.variables['prcp'][40:,:,:,:]
varhis222 = np.nanmean(varhis22, axis=0)
varhis2   = np.broadcast_to(varhis222,(40,12,697,1405))
vardiff2  = varssp2-varhis2
sns.kdeplot(vardiff2.flatten(),color='silver')

varhis33  = f3.variables['prcp'][0:40,:,:,:]
varssp3   = f3.variables['prcp'][40:,:,:,:]
varhis333 = np.nanmean(varhis33, axis=0)
varhis3   = np.broadcast_to(varhis333,(40,12,697,1405))
vardiff3  = varssp3-varhis3
sns.kdeplot(vardiff3.flatten(),color='blue')

varhis44  = f4.variables['prcp'][0:40,:,:,:]
varssp4   = f4.variables['prcp'][40:,:,:,:]
varhis444 = np.nanmean(varhis44, axis=0)
varhis4   = np.broadcast_to(varhis444,(40,12,697,1405))
vardiff4  = varssp4-varhis4
sns.kdeplot(vardiff4.flatten(),color='yellow')

varhis55  = f5.variables['prcp'][0:40,:,:,:]
varssp5   = f5.variables['prcp'][40:,:,:,:]
varhis555 = np.nanmean(varhis55, axis=0)
varhis5   = np.broadcast_to(varhis555,(40,12,697,1405))
vardiff5  = varssp5-varhis5
sns.kdeplot(vardiff5.flatten(),color='red')

varhis66  = f6.variables['prcp'][0:40,:,:,:]
varssp6   = f6.variables['prcp'][40:,:,:,:]
varhis666 = np.nanmean(varhis66, axis=0)
varhis6   = np.broadcast_to(varhis666,(40,12,697,1405))
vardiff6  = varssp6-varhis6
sns.kdeplot(vardiff6.flatten(),color='purple')

plt.xlim(-4,4)
plt.savefig(f'pdf_{vv1}_python_future_change_monthly.pdf')
