#!/bin/python3

import ROOT 

ROOT.gInterpreter.Declare('#include "include/SignalExtractor.h"')
ROOT.gSystem.Load("build/libSignalExtractor.so")

pt_range = [1.5, 2.0]
cent_range = [0, 88]
histname = "r_3_eta_spectrum_pbsc_hist"
input_file = "input_files/19018_combined.root"

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

test_scalings = [0.9 + 0.01 * i for i in range(11)]
output = ROOT.TFile("output.root", "recreate")
for scaling in test_scalings:
    s = ROOT.SignalExtractor(scaling, [0.3, 0.4])
    print(f"Computing for scaling {scaling:.2f}")
    peak, scaled_bg = s.extract(fg, bg);
    peak.SetName(f"peak_scaling_{scaling:.2f}")
    peak.Rebin(5)
    output.WriteTObject(peak)
