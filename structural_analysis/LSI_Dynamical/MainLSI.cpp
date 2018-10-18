/*************************************************************************
 * MainTetrahedral.cpp
 **************************************************************************/

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <assert.h>

#include "Positions.h"
#include "FindHbonds.h"
#include "LocalStructureIndex.h"

int main(int argc, char *argv[]) {

   if (argc != 4) {
      printf("usage: <Gro or XYZ file> <velocity flag or density (g/cc)> <N configs>\n");
      return 1;
   }

   const char *pcConfigFile = argv[1];
   const int iLen = strlen(pcConfigFile);
   const char pcGRO[] = "gro";
   const char pcXYZ[] = "xyz";

   Traj_T traj = NULL;
   if (strcmp(&pcConfigFile[iLen-strlen(pcGRO)], pcGRO) == 0) {
      printf("filetype: gro\n");
      traj = CreateTrajectoryGRO(pcConfigFile, atoi(argv[2]));
   }
   else if (strcmp(&pcConfigFile[iLen-strlen(pcXYZ)], pcXYZ) == 0) {
      printf("filetype: xyz\n");
      traj = CreateTrajectoryXYZ(argv[1], atof(argv[2]));
   }
   else {
      printf("filetype of %s is not currently supported\n", pcConfigFile);
      return 1;
   }

   assert(traj != NULL);

   int iFrames =atoi(argv[3]);
   if (NumFrames(traj) < iFrames) {
      iFrames = NumFrames(traj);
   }

   const double dCut = 4.5;
   const double dLSI_cut = 3.7;

   const char pcOutFile[] = "LSI_op.txt";

   for (int i = 0; i < iFrames; i++) {
      struct WaterSystem* oWaterSys = Frame2Waters(traj->pFrames + i);
      LocalStructureIndex oLSI(oWaterSys, dCut, dLSI_cut);
      std::vector<double> vLSI = oLSI.LSI();

      FILE *pfFile = fopen(pcOutFile, "a");
      fprintf(pfFile, "frame %d: local structure index\n", i);
      double dMeanLSI = 0.0;
      for (int q = 0; q < vLSI.size(); q++) {
	 fprintf(pfFile,"%f \n",vLSI[q]);
	 dMeanLSI += vLSI[q];
      }
      fclose(pfFile);
      dMeanLSI /= (double)vLSI.size();
      printf("frame %d mean LSI: %lf\n",i,dMeanLSI);

      DeleteWaters(oWaterSys);
   }

   FreeTrajectory(traj);

   return 0;
}
