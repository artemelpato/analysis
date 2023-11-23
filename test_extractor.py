#!/bin/python3

import ROOT 

ROOT.gInterpreter.Declare('#include "include/SignalExtractor.h"')
ROOT.gSystem.Load("build/libSignalExtractor.so")

s = ROOT.SignalExtractor(0.98, [0.7, 0.8])
pt_range = [1.0, 1.5]
cent_range = [60, 88]
histname = "eta_spectrum_pbsc_hist"
input_file = "input_files/18724_combined.root"

print(s.get_scaling())
print(s.get_scale_range())

file = ROOT.TFile(input_file, "read");

fg = file.Get(f"{histname}_FG11")
fg = fg.ProjectionX("fg",
    fg.GetYaxis().FindBin(pt_range[0]), fg.GetYaxis().FindBin(pt_range[1]) - 1,
    fg.GetZaxis().FindBin(cent_range[0]), fg.GetZaxis().FindBin(cent_range[1]) - 1)

bg = file.Get(f"{histname}_BG11")
bg = bg.ProjectionX("bg",
    bg.GetYaxis().FindBin(pt_range[0]), bg.GetYaxis().FindBin(pt_range[1]) - 1,
    bg.GetZaxis().FindBin(cent_range[0]), bg.GetZaxis().FindBin(cent_range[1]) - 1)

for h in [fg, bg]: h.Sumw2()

signal, scaled_bg = s.extract(fg, bg)
signal.SetName("signal")
scaled_bg.SetName("scaled_bg");

output = ROOT.TFile("18724_output.root", "recreate");
output.WriteTObject(fg);
output.WriteTObject(bg);
output.WriteTObject(signal);
output.WriteTObject(scaled_bg);

