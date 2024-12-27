import os
import os.path
import re

def ch_trans(filenames,pin_count,site_count):
    #curpath = os.path.dirname(__file__).replace('\\','\\\\')
    curpath = os.path.dirname(filenames).replace('\\','\\\\')
    
    global lineNo 
    global output_flag
    global data_out1
    global data_out2
    global data_out3
    global data_out4
    global cycle_counter
    global transed_data
    global aStringArr
    global aStringLen
    global pin_sum
    global pin_no
    global pin

    lineNo              = 0
    output_flag         = ''
    data_out1           = []
    data_out2           = []
    data_out3           = []
    data_out4           = []
    cycle_counter       = 0
    transed_data        = ''
    aStringArr          = []
    aStringLen          = 0
    pin_sum             =pin_count; #16  #pin数
    pin_no              =site_count; #64  #同测数
    pin             =[]
    pin_name        =[]
    for cycle_counter in range(pin_no):
        pin.append([])
    
    
    #output_file = open(curpath + '\\transed_datalog\\' + 'pin_convert.txt','w')
    output_file = open(curpath + '\\project.dbd','w')
    group_file = open(curpath + '\\Groups_new.spec','w')
    output_file.write('''
dutboard M021_pin {

    sites = '''+ str(site_count) +''';


''')
    group_file.write('''spec Groups {
    group all_pins =  ''')
    
    try:       
        #input_file_1 = open( curpath + '\\raw_data_file_part_1\\' + 'pin.txt','r')
        input_file_1 = open(filenames,'r')
         
    except:
        print('Can\'t open the file!!!!')       
    else:
        pin_sum_count = 0
        pin_no_count = 0
        for line in input_file_1:
            lineNo += 1
            aStringArr  = line.replace('\n','').split("\t")
    
            pin[pin_sum_count].append(aStringArr[1])
            if pin_no_count == 0 : pin_name.append(aStringArr[0])
            pin_sum_count += 1
    
            if pin_sum_count == pin_sum :
                pin_sum_count = 0
                pin_no_count += 1
    
        #group_file.write('//')
        group_file.write(" + ".join(pin_name)+';\n')
        group_file.write('    group DPS_Pins =  ')


        #output_file.write('//')
        for j in range(pin_sum) :
            output_file.write('    signal ')
            output_file.write(pin_name[j])
            output_file.write(''' {
        defaults.protection.disconnectPulldownState = false;
''')
            for i in range(len(pin[j])) :
                if 'P' in pin[j][i]: 
                    channelpre = re.sub('_.*','',pin[j][i])
                    channelpst = re.sub('.*P','',pin[j][i])
                    if len(channelpst)==1 :  channelpst = '0'+ channelpst
                    channel = channelpre +channelpst

                    #write DPS pin
                    if i ==0:group_file.write(pin_name[j]+";")
                else:
                    channel = pin[j][i].replace('D','')
                output_file.write('        site '+ str(i+1) + ' { pogo = '+ channel +'; }\n')
            output_file.write('}\n')
            
        output_file.write('}\n')
        group_file.write('''
    group continuity = all_pins-DPS_Pins;
    group CP_pat = continuity-PA09-PA10-VCAP1_2-VPP;
    group CP_pat_PA09_PA10 = continuity-VCAP1_2-VPP;
    group CP_pat_PA09_PA10_VPP = continuity-VCAP1_2;
//    group DC_SCAN_ALL = PH2 + NRST + VCAP1_2 + PB12 + PB13 + PB14 + PB15 + VPP + PA09 + PA10 + PA13 + MD_DMY + PORDIS ;
//    group DC_SCAN_ALLINPUT = NRST + PORDIS;
////    group DC_SCAN_ALLBIDIR =  VPP + MD_DMY + PA00 + PA02 + PA09 + PA10 + PA11 + PA12 + PA13 + GPIO_LDO;
//    group DC_SCAN_all_functional = PH2 + NRST + VCAP1_2 + PB12 + PB13 + PB14 + PB15 + VPP + PA09 + PA10 + PA13 + MD_DMY + PORDIS ;
//    group AC_SCAN_ALL = PH2 + NRST + VCAP1_2 + PB12 + PB13 + PB14 + PB15 + VPP + PA09 + PA10 + PA13 + MD_DMY + PORDIS ;
//    group AC_SCAN_ALLINPUT = NRST + PORDIS;
////    group AC_SCAN_ALLBIDIR = FTM0 + FTM1 + VPP + MD_DMY + PA00 + PA02 + PA09 + PA10 + PA11 + PA12 + PA13 + GPIO_LDO;
//    group AC_SCAN_all_functional = PH2 + NRST + VCAP1_2 + PB12 + PB13 + PB14 + PB15 + VPP + PA09 + PA10 + PA13 + MD_DMY + PORDIS ;


}
''')
                  
        print('pin.txt' + ' done!')
    finally:
        input_file_1.close()
        output_file.close()
        group_file.close()

def _test():
   
    filen = 'D:/APROJECT/tool/channel_convert_v93k_M039/raw_data_file_part_1/pin_PA8_DPS.txt'
    ch_trans(filen,16,64)


if __name__ == '__main__':
    _test()