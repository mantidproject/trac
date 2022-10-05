diff --git a/Code/Mantid/Framework/DataHandling/src/LoadNexusProcessed.cpp b/Code/Mantid/Framework/DataHandling/src/LoadNexusProcessed.cpp
index e644f68..20915a2 100644
--- a/Code/Mantid/Framework/DataHandling/src/LoadNexusProcessed.cpp
+++ b/Code/Mantid/Framework/DataHandling/src/LoadNexusProcessed.cpp
@@ -34,6 +34,8 @@
 #include "MantidDataObjects/PeakShapeSphericalFactory.h"
 #include "MantidDataObjects/PeakShape.h"
 
+#include <time.h>
+
 namespace Mantid {
 namespace DataHandling {
 
@@ -367,6 +369,9 @@ Workspace_sptr LoadNexusProcessed::doAccelleratedMultiPeriodLoading(
  *  @throw runtime_error Thrown if algorithm cannot execute
  */
 void LoadNexusProcessed::exec() {
+
+    clock_t startt = clock();
+
   progress(0, "Opening file...");
 
   // Throws an approriate exception if there is a problem with file access
@@ -501,6 +506,11 @@ void LoadNexusProcessed::exec() {
   }
 
   m_axis1vals.clear();
+
+  clock_t endt = clock();
+
+  double diffms = ((endt - startt) * 1000) / CLOCKS_PER_SEC;
+  g_log.warning() << "All time = " <<  diffms << std::endl;
 }
 
 /**
@@ -993,8 +1003,13 @@ API::Workspace_sptr LoadNexusProcessed::loadPeaksEntry(NXEntry &entry) {
   // Hop to the right point
   m_cppFile->openPath(entry.path());
   try {
+
+
+
     // This loads logs, sample, and instrument.
     peakWS->loadExperimentInfoNexus(m_cppFile, parameterStr);
+
+
   } catch (std::exception &e) {
     g_log.information("Error loading Instrument section of nxs file");
     g_log.information(e.what());
@@ -1462,8 +1477,19 @@ API::Workspace_sptr LoadNexusProcessed::loadEntry(NXRoot &root,
   m_cppFile->openPath(mtd_entry.path());
   try {
     // This loads logs, sample, and instrument.
+
+      clock_t begininst = clock();
+
+
     local_workspace->loadExperimentInfoNexus(
         m_cppFile, parameterStr); // REQUIRED PER PERIOD
+
+
+    clock_t endinst = clock();
+
+    double diffms = ((endinst - begininst) * 1000) / CLOCKS_PER_SEC;
+    g_log.warning() << "Instrument time = " <<  diffms << std::endl;
+
   } catch (std::exception &e) {
     g_log.information("Error loading Instrument section of nxs file");
     g_log.information(e.what());
@@ -1498,6 +1524,7 @@ API::Workspace_sptr LoadNexusProcessed::loadEntry(NXRoot &root,
   progress(progressStart + 0.2 * progressRange,
            "Reading the workspace history...");
 
+
   return boost::static_pointer_cast<API::Workspace>(local_workspace);
 }
 
