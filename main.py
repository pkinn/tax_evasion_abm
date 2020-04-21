from abm_classes import Government, Firm
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


def update_govs(gov_list):
    for gg in gov_list:
        gg.rate += np.random.uniform(-0.1,0.1, size = gg.rate.shape)


def update_firms(firm_list):
    for ff in firm_list:
        ff.allocation += np.random.uniform(-10, 10, size = ff.allocation.shape)


def pay_taxes(gov_list, firm_list):
    for gg in range(len(gov_list)):
        for ff in range(len(firm_list)):
            fidx = firm_list[ff].id
            gidx = gov_list[gg].id
            transaction_amount = gov_list[gg].rate[fidx] * firm_list[ff].allocation[gidx]
            gov_list[gg].resources += transaction_amount
            firm_list[ff].resources -= transaction_amount


## Parameters to define
# Parameters about the simulation
n_gov = 5
n_firm = 3
n_time = 100
tax_iter = 5
init_resource_firm = np.random.uniform(100, 500, (n_firm, 1))
init_resource_gov = np.random.uniform(200, 300, (n_gov, 1))

# Holders for data collected during the run
allocation = np.zeros([n_firm, n_gov, n_time])
rate = np.zeros([n_firm, n_gov, n_time])
n_gov_max = 100
n_firm_max = 100
gov_resources = np.zeros([n_time, n_gov_max])
firm_resources = np.zeros([n_time, n_firm_max])
print(gov_resources.shape)

## Initialize run
gov_list = []
firm_list = []
for ii in range(n_gov):
    rate_init = np.random.uniform(0, 1, (n_firm, 1))
    gov_list.append(Government(ii, init_resource_gov[ii], rate_init))
    print(gov_list[ii].id)
for ii in range(n_firm):
    allocation_init = np.random.uniform(0, 1, (n_gov, 1))
    firm_list.append(Firm(ii, init_resource_firm[ii], allocation_init))
    print(firm_list[ii].id)

## Run simulation
for ii in range(n_time):
    # print('ii = ' + str(ii))
    # print(id_list)
    update_govs(gov_list)
    update_firms(firm_list)
    if ii % tax_iter:
        pay_taxes(gov_list, firm_list)

    for gg in range(len(gov_list)):
        # print('gg = ' + str(gg))

        gidx = gov_list[gg].id
        gov_resources[ii, gidx] = gov_list[gg].resources
        for ff in range(n_firm):
            # print('ff = ' + str(ff))
            fidx = firm_list[ff].id
            rate[fidx, gidx, ii] = gov_list[gg].rate[fidx]
            allocation[fidx, gidx, ii] = firm_list[ff].allocation[gidx]
            firm_resources[ii, fidx] = firm_list[ff].resources
    gidx_list = [g.id for g in gov_list]
    fidx_list = [f.id for f in firm_list]
    max_govt = np.max([n_gov, max(gidx_list)])
    max_firm = np.max([n_firm, max(fidx_list)])

## After simulation, trim firm_resources, gov_resources, rate, allocation
firm_resources = firm_resources[:, 0:max_firm]
gov_resources = gov_resources[:, 0:max_govt]
rate = rate[0:max_firm, 0:max_govt, :]
allocation = allocation[0:max_firm, 0:max_govt, :]

## Plot things
print(str(allocation[1, :, :]))
plt.figure(1)
plt.plot(allocation[1, :, :])
plt.show()

plt.figure()
plt.plot(gov_resources)
plt.title('resources')
plt.legend([str(x.id) for x in gov_list])
plt.show()
