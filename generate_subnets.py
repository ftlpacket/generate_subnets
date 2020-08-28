from netaddr import *
import json

def generate_subnets(office_supernet):

    subnets = list(office_supernet.subnet(24))
    count = 1
    data = {}
    
    for subnet in subnets:
        if count == 1:
            data.update(data_subnet = str(subnet[0]),
                        data_mask = str(subnet.netmask),
                        data_gateway = str(subnet[1]),
                        data_dhcp_exclude_start = str(subnet[1]),
                        data_dhcp_exclude_end = str(subnet[5]))
            
            #print(data)
        if count == 2:
            data.update(voice_subnet = str(subnet[0]),
                        voice_mask = str(subnet.netmask),
                        voice_gateway = str(subnet[1]),
                        voice_dhcp_exclude_start = str(subnet[1]),
                        voice_dhcp_exclude_end = str(subnet[5]))
            
            #print(data)
        if count == 3:
            new_count = 1
            smaller_subnets = list(subnet.subnet(26))

            for net in smaller_subnets:
                if new_count == 1:
                    data.update(infra_subnet = str(net[0]),
                                infra_mask = str(net.netmask),
                                infra_gateway = str(net[1]),
                                infra_dhcp_exclude_start = str(net[1]),
                                infra_dhcp_exclude_end = str(net[5])) 
                    
                    #print(data)
                if new_count == 2:
                    data.update(iot_subnet = str(net[0]),
                                iot_mask = str(net.netmask),
                                iot_gateway = str(net[1]))
                
                new_count += 1
        if count == 4:
            count_3 = 1
            medium_subnets = list(subnet.subnet(25))
            transit_subnets = list(medium_subnets[1].subnet(26))
            
            for p2p in list(transit_subnets[0].subnet(30)):
                if count_3 == 1:
                    data.update(corp_rt01_uplink_subnet = str(p2p[0]),
                                corp_rt01_uplink_ip = str(p2p[2]))
                if count_3 == 2:
                    data.update(corp_rt02_uplink_subnet = str(p2p[0]),
                                corp_rt02_uplink_ip = str(p2p[2])) 
                if count_3 == 3: 
                    data.update(guest_rt01_uplink_subnet = str(p2p[0]),
                                guest_rt01_uplink_ip = str(p2p[2])) 
                if count_3 == 4: 
                    data.update(guest_rt02_uplink_subnet = str(p2p[0]),
                                guest_rt02_uplink_ip = str(p2p[2]))                  
                count_3 += 1
            
            loopback_subnets = list(transit_subnets[1].subnet(27))

            count_4 = 1

            for loopback in list(loopback_subnets[1].subnet(32)):
                if count_4 == 5:
                    data.update(mgmt_loopback0_ip = str(loopback[0]),
                                corp_ospf_router_id = str(loopback[0]))
                if count_4 == 6:
                    data.update(guest_ospf_router_id = str(loopback[0]))
                count_4 += 1

        count += 1

    return data
        

def main():
    office_supernet = IPNetwork('10.199.48.0/22')
    
    state = generate_subnets(office_supernet)

    print(json.dumps(state, indent=2))

if __name__ == "__main__":
    main()