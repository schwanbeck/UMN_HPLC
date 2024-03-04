from tools.plot import plot_images
from tools.tools import open_file, DF_TIME, DF_DATA_POINTS, DF_CHANNEL
from hplc.quant import Chromatogram

time = 'time'
signal = 'signal'

for lac, ac, file in [
    # (20, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-10-2023 4-59-39 PMSystem001.dat.asc'),
    # (0, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-10-2023 5-42-41 PMSystem002.dat.asc'),
    # (15, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-10-2023 6-25-34 PMSystem003.dat.asc'),
    # (10, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-10-2023 7-08-29 PMSystem004.dat.asc'),
    # (5, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-10-2023 7-51-28 PMSystem005.dat.asc'),
    (1, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-10-2023 8-34-26 PMSystem006.dat.asc'),
    # (0.5, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-10-2023 9-17-19 PMSystem007.dat.asc'),
    # (0.1, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-10-2023 10-00-13 PMSystem008.dat.asc'),
    # (0.01, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-10-2023 10-43-06 PMSystem009.dat.asc'),
    # (0, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-10-2023 11-25-58 PMSystem010.dat.asc'),
    # (1, 1, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 12-08-49 AMSystem001.dat.asc'),
    # (0, 20, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 12-51-46 AMSystem002.dat.asc'),
    # (0, 15, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 1-34-45 AMSystem003.dat.asc'),
    # (0, 10, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 2-17-40 AMSystem004.dat.asc'),
    # (0, 5, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 3-00-32 AMSystem005.dat.asc'),
    # (0, 1, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 3-43-25 AMSystem006.dat.asc'),
    # (0, 0.5, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 4-26-18 AMSystem007.dat.asc'),
    # (0, 0.1, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 5-09-11 AMSystem008.dat.asc'),
    # (0, 0.01, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 5-52-04 AMSystem009.dat.asc'),
    # (0, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 6-35-02 AMSystem010.dat.asc'),
    # (0, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 7-17-57 AMSystem011.dat.asc'),
    # (20, 20, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 8-00-54 AMSystem002.dat.asc'),
    # (10, 10, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 8-43-49 AMSystem003.dat.asc'),
    # (5, 5, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 9-26-42 AMSystem004.dat.asc'),
    # (20, 1, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 10-09-35 AMSystem005.dat.asc'),
    # (1, 20, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 10-52-29 AMSystem006.dat.asc'),
    # (5, 15, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 11-35-20 AMSystem007.dat.asc'),
    # (15, 5, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 12-18-14 PMSystem008.dat.asc'),
    # (0.01, 20, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 1-01-11 PMSystem009.dat.asc'),
    # (20, 0.01, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 1-44-06 PMSystem010.dat.asc'),
    # (0, 0, '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231010_LActate_Acetate_Reference/10-11-2023 2-26-59 PMSystem011.dat.asc'),
]:
    infos, df_all = open_file(file)
    df_all[DF_TIME] = df_all[DF_TIME] / 60
    df = df_all.loc[df_all[DF_CHANNEL] == 0, [DF_TIME, DF_DATA_POINTS]].rename(columns={
        DF_TIME: time,
        DF_DATA_POINTS: signal,
    })
    chrom = Chromatogram(df)
    chrom.crop([6, 15])
    peaks = chrom.fit_peaks(buffer=0)
    print(peaks.head(100))
    chrom.show()
    print(ac, lac, '\n', peaks.head(100))

# if __name__ == '__main__':
#     _testf = '/home/schwan/PycharmProjects/UMN_HPLC/TEST/20231018_Reactor_Analysis_Lactate_Acetate/Ch1_13_40minTest5_Lactate_Acetate_210_254.met_004.dat.asc'
#     infos, df = open_file(_testf)
#     plot_images('test', infos, df, [0, 1, 2], [0, 1, 2], None)


