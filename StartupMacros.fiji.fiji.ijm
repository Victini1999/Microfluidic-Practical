run("Clear Results");
///// Set the scale and measures of interest
run("Duplicate...");
run("Set Scale...", "distance=27 known=30 unit=um");      //pour paramétrer l'échelle de longueur
makeLine(135, 35, 600, 35);
run("Set Measurements...", "Min&gray value mean Gray value=None decimal=3");
run("Measure");
list = getList("image.titles");

    selectWindow("Results");
    ///// Save data
    saveAs("Results", Nom);
    ///// Close everything
    selectWindow("Results");

