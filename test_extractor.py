#!/bin/python3

import ROOT 
import numpy as np

ROOT.gInterpreter.Declare('#include "include/SignalExtractor.h"')
ROOT.gSystem.Load("build/libSignalExtractor.so")

pt_range = [4.0, 4.5]

cent_ranges = [[0, 88],
               [0, 20],
               [20, 40],
               [40, 60],
               [60, 88]]

cut_type = "r_2"

histname = f"{cut_type}_eta_spectrum_pbsc_hist"
input_file = f"input_files/19036_{cut_type}.root"
output_file = f"{cut_type}_output.root"

file = ROOT.TFile(input_file, "read");

test_scalings = np.arange(0.9, 1.2, 0.01)

output = ROOT.TFile(output_file, "recreate")

for cent_range in cent_ranges:
    fg = file.Get(f"{histname}_FG11")
    fg = fg.ProjectionX("fg_{}_{}".format(*cent_range),
        fg.GetYaxis().FindBin(pt_range[0]), fg.GetYaxis().FindBin(pt_range[1]) - 1,
        fg.GetZaxis().FindBin(cent_range[0]), fg.GetZaxis().FindBin(cent_range[1]) - 1)

    bg = file.Get(f"{histname}_BG11")
    bg = bg.ProjectionX("bg_{}_{}".format(*cent_range),
        bg.GetYaxis().FindBin(pt_range[0]), bg.GetYaxis().FindBin(pt_range[1]) - 1,
        bg.GetZaxis().FindBin(cent_range[0]), bg.GetZaxis().FindBin(cent_range[1]) - 1)

    for h in [fg, bg]:
        h.Sumw2()
        
    for scaling in test_scalings:
        s = ROOT.SignalExtractor(scaling, [0.7, 0.8])
        print(f"Computing for scaling {scaling:.3f}")
        peak, scaled_bg = s.extract(fg, bg);

        name = "peak_scaling_{:.3f}_cent_{}_{}".format(scaling, *cent_range)
        peak.SetName(name)

        peak.Rebin(5)
        peak.GetXaxis().SetRangeUser(0.4, 0.7)
        output.WriteTObject(peak)

    del fg
    del bg
