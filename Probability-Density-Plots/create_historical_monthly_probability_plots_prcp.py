import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read monthly data from each experiment for the given variable
vv1 = "prcp"
fD = nc.Dataset(f'../analysis/netcdf/Daymet_1980-2019_{vv1}.nc')
fL = nc.Dataset(f'../analysis/netcdf/Livneh_1980-2018_{vv1}.nc')
f1 = nc.Dataset(f'../analysis/netcdf/CMIP6_1980-2059_{vv1}.nc')
f2 = nc.Dataset(f'../analysis/netcdf/RegCM_1980-2059_{vv1}.nc')
f3 = nc.Dataset(f'../analysis/netcdf/Livneh_RegCM_1980-2059_{vv1}.nc')
f4 = nc.Dataset(f'../analysis/netcdf/Daymet_RegCM_1980-2059_{vv1}.nc')
f5 = nc.Dataset(f'../analysis/netcdf/Livneh_DBCCA_1980-2059_{vv1}.nc')
f6 = nc.Dataset(f'../analysis/netcdf/Daymet_DBCCA_1980-2059_{vv1}.nc')

# Create the probability density plots for the historical period
varD1 = fD.variables['prcp'][:,:,:,:]
sns.kdeplot(varD1.flatten(),color='green')

varL1 = fL.variables['prcp'][:,:,:,:]
sns.kdeplot(varL1.flatten(),color='black')

var11 = f1.variables['pr'][0:40,:,:,:]
sns.kdeplot(var11.flatten(),color='dimgray')

var21 = f2.variables['prcp'][0:40,:,:,:]
sns.kdeplot(var21.flatten(),color='silver')

var31 = f3.variables['prcp'][0:40,:,:,:]
sns.kdeplot(var31.flatten(),color='blue')

var41 = f4.variables['prcp'][0:40,:,:,:]
sns.kdeplot(var41.flatten(),color='yellow')

var51 = f5.variables['prcp'][0:40,:,:,:]
sns.kdeplot(var51.flatten(),color='red')

var61 = f6.variables['prcp'][0:40,:,:,:]
sns.kdeplot(var61.flatten(),color='purple')

plt.xlim(0,40)
plt.savefig(f'pdf_{vv1}_python_historical_monthly.pdf')
