import ROOT 

ROOT.gInterpreter.Declare('#include "include/SignalExtractor.h"')
ROOT.gSystem.Load("build/libSignalExtractor.so")

s = ROOT.SignalExtractor(1.0, [0.7, 0.8])

print(s.scaling())
print(s.scale_range())

file = ROOT.TFile("input_files/18724_combined.root", "read");

fg = file.Get("eta_spectrum_pbsc_hist_FG11")
fg = fg.ProjectionX("fg",
    fg.GetYaxis().FindBin(4.0), fg.GetYaxis().FindBin(5.0) - 1,
    fg.GetZaxis().FindBin(0), fg.GetZaxis().FindBin(88) - 1)

bg = file.Get("eta_spectrum_pbsc_hist_BG11")
bg = bg.ProjectionX("bg",
    bg.GetYaxis().FindBin(4.0), bg.GetYaxis().FindBin(5.0) - 1,
    bg.GetZaxis().FindBin(0), bg.GetZaxis().FindBin(88) - 1)

signal, scaled_bg = s.extract(fg, bg)
signal.SetName("signal")
scaled_bg.SetName("scaled_bg");

output = ROOT.TFile("test_extractor_output.root", "recreate");
output.WriteTObject(fg);
output.WriteTObject(bg);
output.WriteTObject(signal);
output.WriteTObject(scaled_bg);

