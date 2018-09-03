import pandas as pd
from zipfile import ZipFile
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools


class AutoFilter:
    def __init__(self, data_frame, tc_list, plot_dir):
        """
        Given the two class arguments, data_frame and tc_list (test condition list), where tc_list is the
        important column headers of the DataFrame, iterate through the list and create a list of unique
        properties for each tc.  Each dictionary value is accessible with data attributes.  The data attributes
        return a tuple with the test condition at index 0 and the unique values at index 1
        (i.e. ('Serial Number', ['23AC', '2450'])).

        Each of the graph types is a list of tuples which are used in the corresponding method to create the
        required graphs and return the DataFrame for those waveforms.
        """

        cond_dict = {}
        for i, condition in enumerate(tc_list):
            cond_dict[condition] = list(data_frame[condition].unique())
        self.cond_dict = cond_dict

        # Data Attributes
        self.dut = ('DUT', cond_dict['DUT'])
        self.sn = ('Serial_Number', cond_dict['Serial_Number'])
        self.tp = ('Test_Points', cond_dict['Test_Points'])
        self.slew = ('Slew_1', cond_dict['Slew_1'])
        self.temp = ('Temperature_Setpoint', cond_dict['Temperature_Setpoint'])
        self.ts = ('Test_Station', cond_dict['Test_Station'])
        try:
            self.v1 = ('Voltage_1', cond_dict['Voltage_1'])
        except KeyError:
            print(f'No Voltage_1')
        try:
            self.v2 = ('Voltage_2', cond_dict['Voltage_2'])
        except KeyError:
            print(f'No Voltage_2')
        try:
            self.v3 = ('Voltage_3', cond_dict['Voltage_3'])
        except KeyError:
            print(f'No Voltage_3')
        try:
            self.v4 = ('Voltage_4', cond_dict['Voltage_4'])
        except KeyError:
            print(f'No Voltage_4')

        # Graph Types - i.e. test point and slew or test point and temp
        self.tp_slew_list = [self.tp, self.slew]
        self.tp_temp_list = [self.tp, self.temp]
        self.seq_list = [self.slew, self.v1]
        self.all_list = [self.sn, self.tp, self.v1, self.temp, self.slew]

        self.plot_dir = plot_dir
        self.df = data_frame

    def read_waveform(self, data_address):
        """
        Uses numpy to create an array for the specified waveform
        :param data_address: string -> path and file name
        :return: np.array of floats
        """
        f = ZipFile(os.path.join(data_address), 'r')
        f_name = f.namelist()
        w = f.read(f_name[0])  # the key is the file name without the 'bin' extension (i.e. CH1)
        f.close()
        dt = np.dtype(float)
        dt = dt.newbyteorder('>')
        wf = np.frombuffer(w, dtype=dt)
        return wf

    def calculate_time(self, ix, xi, wf):
        """
        Given initial x and x increment, all the x (time) values
        are calculated for the waveform
        :param ix: initial x - float
        :param xi: x increment - float
        :param wf: waveform - np.array
        :return x_time: np.array x component for each value of the wf
        """
        wf_len = len(wf)
        x_time = np.arange(ix, (ix + wf_len * xi), xi)
        return x_time

    def create_wf_df(self, df_filter):
        """
        Given a DataFrame (i.e. df_filter) this method:
        1) looks at the data_address column
        2) send the address to read_waveform which retuns a 1 by x array of the waveform data points
        3) the array is added to a DataFrame
        4) the waveform, xi and ix is sent to calculate_time which returns an array of time (x) values
        5) a time column is added to the DataFrame for each waveform column
        6) the DataFrame of waveforms and time is returned
        :param df_filter: Pandas.DataFrame
        :return df_wf: Pandas.DataFrame
        """
        df_wf = pd.DataFrame()
        wf_length_count = {}
        for i, v in enumerate(df_filter['data_address']):
            wf = self.read_waveform(v)
            wf_len = len(wf)
            if wf_len not in wf_length_count:
                wf_length_count[wf_len] = 1
            else:
                wf_length_count[wf_len] += 1
            if i == 0:
                first_wf_len = wf_len  # length of first waveform
            x_time = self.calculate_time(ix=list(df_filter['initial_x'])[i], xi=list(df_filter['x_increment'])[i],
                                         wf=wf)
            try:
                df_wf[f'ch_{i}'] = wf
                df_wf[f'time_{i}'] = x_time
            except ValueError:
                print("The number of data points in the waveform doesn't match the length of the DataFrame, ")
                print(f"which is {first_wf_len} points.")
                pass
        print(wf_length_count)
        return df_wf

    def make_dir(self, save_name):
        directory = '\\'.join(save_name.split('\\')[:-1])
        if not os.path.exists(directory):
            os.makedirs(directory)

    def plot(self, df_wf, save_name):
        # Plot Waveforms
        plt.figure(figsize=(10, 8))
        cnt = int(len(df_wf.columns) / 2)
        # Plot each channel in the figure
        for x in range(0, cnt):
            plt.plot(df_wf[f'time_{x}'], df_wf[f'ch_{x}'])
        y_scale = max(df_wf.max()) + 0.5
        if y_scale >= 6:
            step = 1
        elif 3 <= y_scale < 6:
            step = 0.5
        else:
            step = 0.25
        major_ticks = np.arange(0, y_scale, step)  # y_scale/12
        if len(df_wf.columns) / 2 < 10:
            plt.legend()
        plt.xlabel('Time(s)')
        plt.ylabel('Voltage(V)')
        plt.yticks(major_ticks)
        plt.grid()
        #         plt.show()
        self.make_dir(save_name)
        plt.savefig(f'{save_name}.png')
        plt.close()

    def iter_filter(self, test_tuple, params, dirs, create_df):
        df_dict = {}
        dirs = os.path.join(self.plot_dir, dirs)
        for i in itertools.product(*[b for _, b in test_tuple]):
            print('\n'.join(f'{a}:{b}' for a, b in zip(params, i)))  # keep - used for printing information only
            name_params = '_'.join(f'{b}{a}' for a, b in zip(params, i))  # keep - this is used
            save_name = f'{dirs}\\{self.dut[1][0]}_{name_params}'.replace('.', 'p')

            filter_t = ' & '.join(f'{c[0]} == "{b}"' for b, c in zip(i, test_tuple))
            print(f'filter_t: {filter_t}')
            filtered_df = self.df.loc[self.df.eval(filter_t)]

            waveform_df = self.create_wf_df(filtered_df)
            if len(waveform_df) == 0:
                print('*' * 10, ' Filter Conditions Result in Empty DataFrame', '*' * 10)
            else:
                if create_df:
                    df_dict[name_params] = waveform_df
                self.plot(waveform_df, save_name)
        print('Finished')
        if create_df:
            return df_dict

    def seq(self, create_df=False):
        params = ['slew', 'v1']
        dirs = 'startup\\sequencing'
        df_dict = self.iter_filter(self.seq_list, params, dirs, create_df)
        return df_dict

    def tp_slew(self, create_df=False):
        params = ['tp', 'slew']
        dirs = 'startup\\tp_slew'
        df_dict = self.iter_filter(self.tp_slew_list, params, dirs, create_df)
        return df_dict

    def tp_temp(self, create_df=False):
        params = ['tp', 'temp']
        dirs = 'startup\\tp_temp'
        df_dict = self.iter_filter(self.tp_temp_list, params, dirs, create_df)
        return df_dict

    def all_test_conditions(self, create_df=False):
        params = ['sn', 'tp', 'v1', 'temp', 'slew']
        dirs = 'startup\\all_wf'
        df_dict = self.iter_filter(self.all_list, params, dirs, create_df)
        return df_dict
