#!/bin/python3

import ROOT 

ROOT.gInterpreter.Declare('#include "include/SignalExtractor.h"')
ROOT.gSystem.Load("build/libSignalExtractor.so")

pt_range = [1.0, 1.5]
cent_range = [0, 88]

cut_type = "r_4"

histname = f"{cut_type}_eta_spectrum_pbsc_hist"
input_file = f"input_files/19036_{cut_type}.root"
output_file = f"{cut_type}_output.root"

file = ROOT.TFile(input_file, "read");

fg = file.Get(f"{histname}_FG11")
fg = fg.ProjectionX("fg",
    fg.GetYaxis().FindBin(pt_range[0]), fg.GetYaxis().FindBin(pt_range[1]) - 1,
    fg.GetZaxis().FindBin(cent_range[0]), fg.GetZaxis().FindBin(cent_range[1]) - 1)

bg = file.Get(f"{histname}_BG11")
bg = bg.ProjectionX("bg",
    bg.GetYaxis().FindBin(pt_range[0]), bg.GetYaxis().FindBin(pt_range[1]) - 1,
    bg.GetZaxis().FindBin(cent_range[0]), bg.GetZaxis().FindBin(cent_range[1]) - 1)

for h in [fg, bg]:
    h.Sumw2()

test_scalings = [0.96 + 0.001 * i for i in range(21)]
output = ROOT.TFile(output_file, "recreate")
for scaling in test_scalings:
    s = ROOT.SignalExtractor(scaling, [0.3, 0.4])
    print(f"Computing for scaling {scaling:.3f}")
    peak, scaled_bg = s.extract(fg, bg);
    peak.SetName(f"peak_scaling_{scaling:.3f}")
    peak.Rebin(5)
    peak.GetXaxis().SetRangeUser(0.4, 0.7)
    output.WriteTObject(peak)
