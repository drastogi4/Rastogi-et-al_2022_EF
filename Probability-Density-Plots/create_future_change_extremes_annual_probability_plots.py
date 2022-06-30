import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#input extreme indices
var   = ("p95","t95","numdays_above_t95","t05","numdays_below_t05","p95","numdays_above_p95")

fig, ax = plt.subplots(3, 2, figsize=(11,8))
for i in np.arange(np.shape(var)[0]):
#assign axis
    if(var[i] == "p95"):
        xx = 2
        yy = 0
        ax[xx,yy].set_xlim(-12,16)
    if(var[i] == "t95"):
        xx = 0
        yy = 0
        ax[xx,yy].set_xlim(-1,7)
    if(var[i] == "t05"):
        xx = 1
        yy = 0
        ax[xx,yy].set_xlim(-2,10)
    if(var[i] == "numdays_below_t05"):
        xx = 1
        yy = 1
        ax[xx,yy].set_xlim(-20,5)
    if(var[i] == "numdays_above_t95"):
        xx = 0
        yy = 1
        ax[xx,yy].set_xlim(-20,80)
    if(var[i] == "numdays_above_p95"):
        xx = 2
        yy = 1
        ax[xx,yy].set_xlim(-4,7)
    vv = var[i]
#Read future changes for each experiment
    f1 = nc.Dataset(f'../analysis/netcdf/CMIP6_ssp_minus_his_{vv}.nc')
    f2 = nc.Dataset(f'../analysis/netcdf/RegCM_ssp_minus_his_{vv}.nc')
    f3 = nc.Dataset(f'../analysis/netcdf/Livneh_RegCM_ssp_minus_his_{vv}.nc')
    f4 = nc.Dataset(f'../analysis/netcdf/Daymet_RegCM_ssp_minus_his_{vv}.nc')
    f5 = nc.Dataset(f'../analysis/netcdf/Livneh_DBCCA_ssp_minus_his_{vv}.nc')
    f6 = nc.Dataset(f'../analysis/netcdf/Daymet_DBCCA_ssp_minus_his_{vv}.nc')

#create probability density plots
    vardiff1 = np.asarray(f1.variables[f'{vv}'][:,:,:])
    vardiff1 = np.where(vardiff1 == -999.,np.nan,vardiff1)
    sns.kdeplot(vardiff1.flatten(),color='dimgray',ax=ax[xx,yy])

    vardiff2 = np.asarray(f2.variables[f'{vv}'][:,:,:])
    vardiff2 = np.where(vardiff2 == -999.,np.nan,vardiff2)
    sns.kdeplot(vardiff2.flatten(),color='silver',ax=ax[xx,yy])

    vardiff3 = np.asarray(f3.variables[f'{vv}'][:,:,:])
    vardiff3 = np.where(vardiff3 == -999.,np.nan,vardiff3)
    sns.kdeplot(vardiff3.flatten(),color='blue',ax=ax[xx,yy])

    vardiff4 = np.asarray(f4.variables[f'{vv}'][:,:,:])
    vardiff4 = np.where(vardiff4 == -999.,np.nan,vardiff4)
    sns.kdeplot(vardiff4.flatten(),color='yellow',ax=ax[xx,yy])

    vardiff5 = np.asarray(f5.variables[f'{vv}'][:,:,:])
    vardiff5 = np.where(vardiff5 == -999.,np.nan,vardiff5)
    sns.kdeplot(vardiff5.flatten(),color='red',ax=ax[xx,yy])

    vardiff6 = np.asarray(f6.variables[f'{vv}'][:,:,:])
    vardiff6 = np.where(vardiff6 == -999.,np.nan,vardiff6)
    sns.kdeplot(vardiff6.flatten(),color='purple',ax=ax[xx,yy])

    ax[xx,yy].set_title(f'{var[i]}')
    del vardiff1, vardiff2, vardiff3, vardiff4, vardiff5, vardiff6
plt.savefig(f'pdf_extremes_annual_change.pdf')
