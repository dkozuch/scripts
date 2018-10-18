/***************************************************************************
 * FindHbonds.h
 *
 ***************************************************************************/

#include <cstdio>
#include <cmath>
#include <vector>
#include <cassert>

#include "Positions.h"
#include "FindHbonds.h"

/***************************************************************************/

struct WaterSystem* Frame2Waters(const Frame_T pFrame) {
   assert(pFrame != NULL);

   const int iOxyType = 2; // Problem SPECIFIC!!

   // find number of waters
   int iWaters = 0;
   for (int i = 0; i < pFrame->iN; i++) {
      if (pFrame->piType[i] == iOxyType) {
	 iWaters++;
      }
   }

   // santiy check
   if (iWaters == 0) {
      printf("Frame has zero water molecules!\n");
      return NULL;
   }
   //printf("num waters: %d\n", iWaters);
   const int nWaters = iWaters;

   // populate positions of water molecules
   int off1 = 0, off2 = 0;
   if (pFrame->piType[0] == iOxyType) {
      off1 = 1;
      off2 = 2;
   }
   else {
      off1 = -1;
      off2 = 1;
   }

   Water* oWaters = new Water[nWaters];
   int water = 0;
   for (int i = 0; i < pFrame->iN; i++) {
      if (pFrame->piType[i] == iOxyType) {
	 oWaters[water].pdO[0] = pFrame->pdX[i];
	 oWaters[water].pdO[1] = pFrame->pdY[i];
	 oWaters[water].pdO[2] = pFrame->pdZ[i];
	 oWaters[water].pdH1[0] = pFrame->pdX[i+off1];
	 oWaters[water].pdH1[1] = pFrame->pdY[i+off1];
	 oWaters[water].pdH1[2] = pFrame->pdZ[i+off1];
	 oWaters[water].pdH2[0] = pFrame->pdX[i+off2];
	 oWaters[water].pdH2[1] = pFrame->pdY[i+off2];
	 oWaters[water].pdH2[2] = pFrame->pdZ[i+off2];
	 water++;
      }
   }

   struct WaterSystem* oWaterSys = new struct WaterSystem;
   oWaterSys->pH20 = oWaters;
   oWaterSys->N = nWaters;
   for (int i = 0; i < 3; i++) {
      oWaterSys->pdBox[i] = pFrame->pdBox[i];
   }

   return oWaterSys;
}

/***************************************************************************/

void DeleteWaters(struct WaterSystem* oWaterSys) {
   assert(oWaterSys != NULL);

   delete [] oWaterSys->pH20;
   delete oWaterSys;
}
/***************************************************************************/

struct AdjMat* FindHbonds(const struct WaterSystem* oWaterSys) {
   assert(oWaterSys != NULL);

   const struct Water* oWaters = oWaterSys->pH20;
   const int nWaters = oWaterSys->N;

   // allocate and initialize adjacency matrix
   unsigned int ** ppiAdjMat = new unsigned int* [nWaters];
   for (int i = 0; i < nWaters; i++) {
      ppiAdjMat[i] = new unsigned int [nWaters];
      for (int j = 0; j < nWaters; j++) {
	 ppiAdjMat[i][j] = 0;
      }
   }

   // populate matrix 
   const double dRooCut_2 = 3.5*3.5;
   const double dCosCut = 0.86602540378; // cos(30 degress)

   for(int i = 0; i < nWaters; i++) {
      double rOH1_i[3], rOH2_i[3];
      for (int n = 0; n < 3; n++) {
	 rOH1_i[n] = oWaters[i].pdH1[n] - oWaters[i].pdO[n];
	 rOH2_i[n] = oWaters[i].pdH2[n] - oWaters[i].pdO[n];
	 rOH1_i[n] -= oWaterSys->pdBox[n]*round(rOH1_i[n] / oWaterSys->pdBox[n]);
	 rOH2_i[n] -= oWaterSys->pdBox[n]*round(rOH2_i[n] / oWaterSys->pdBox[n]);
      }
      for (int j = i+1; j < nWaters; j++) {
	 double dXYZ[3];
	 double dRoo_2 = 0.0;
	 for (int n = 0; n < 3; n++) {
	    dXYZ[n] = oWaters[j].pdO[n] - oWaters[i].pdO[n];
	    dXYZ[n] -= oWaterSys->pdBox[n]*round(dXYZ[n] / oWaterSys->pdBox[n]);;
	    dRoo_2 += dXYZ[n]*dXYZ[n];
	 }
	 if (dRoo_2 <= dRooCut_2) {
	    double rOH1_j[3], rOH2_j[3];
	    for (int n = 0; n < 3; n++) {
	       rOH1_j[n] = oWaters[j].pdH1[n] - oWaters[j].pdO[n];
	       rOH2_j[n] = oWaters[j].pdH2[n] - oWaters[j].pdO[n];
	       rOH1_j[n] -= oWaterSys->pdBox[n]*round(rOH1_j[n] / oWaterSys->pdBox[n]);
	       rOH2_j[n] -= oWaterSys->pdBox[n]*round(rOH2_j[n] / oWaterSys->pdBox[n]);
	    } 
	    double dotH1_i = 0.0;
	    double dotH2_i = 0.0;
	    double dotH1_j = 0.0;
	    double dotH2_j = 0.0;
	    for (int n = 0; n < 3; n++) {
	       dotH1_i += rOH1_i[n]*dXYZ[n];
	       dotH2_i += rOH2_i[n]*dXYZ[n];
	       dotH1_j -= rOH1_j[n]*dXYZ[n];
	       dotH2_j -= rOH2_j[n]*dXYZ[n];
	    }

	    //const double rOH = 0.9572; // TIP4P2005
	    const double dRoo = sqrt(dRoo_2);
	    double cosT = -1.0;
	    if (dotH1_i > 0) {
	       double rOH_2 = rOH1_i[0]*rOH1_i[0] + rOH1_i[1]*rOH1_i[1] + rOH1_i[2]*rOH1_i[2];
	       //cosT = dotH1_i/(rOH*dRoo);
	       cosT = dotH1_i/(sqrt(rOH_2)*dRoo);
	       if (cosT >= dCosCut) {
		  ppiAdjMat[i][j] = 1;
		  ppiAdjMat[j][i] = 1;
		  continue;
	       }
	    }
	    if (dotH2_i > 0) {
	       double rOH_2 = rOH2_i[0]*rOH2_i[0] + rOH2_i[1]*rOH2_i[1] + rOH2_i[2]*rOH2_i[2];
	       //cosT = dotH2_i/(rOH*dRoo);
	       cosT = dotH2_i/(sqrt(rOH_2)*dRoo);
	       if (cosT >= dCosCut) {
		  ppiAdjMat[i][j] = 1;
		  ppiAdjMat[j][i] = 1;
		  continue;
	       }
	    }
	    if (dotH1_j > 0) {
	       double rOH_2 = rOH1_j[0]*rOH1_j[0] + rOH1_j[1]*rOH1_j[1] + rOH1_j[2]*rOH1_j[2];
	       //cosT = dotH1_j/(rOH*dRoo);
	       cosT = dotH1_j/(sqrt(rOH_2)*dRoo);
	       if (cosT >= dCosCut) {
		  ppiAdjMat[i][j] = 1;
		  ppiAdjMat[j][i] = 1;
		  continue;
	       }
	    }
	    if (dotH2_j > 0) {
	       double rOH_2 = rOH2_j[0]*rOH2_j[0] + rOH2_j[1]*rOH2_j[1] + rOH2_j[2]*rOH2_j[2];
	       //cosT = dotH2_j/(rOH*dRoo);
	       cosT = dotH2_j/(sqrt(rOH_2)*dRoo);
	       if (cosT >= dCosCut) {
		  ppiAdjMat[i][j] = 1;
		  ppiAdjMat[j][i] = 1;
		  continue;
	       }
	    }
	 }
      }
   }

   struct AdjMat* oAdjMat =  new struct AdjMat;
   oAdjMat->ppiAdjMat = ppiAdjMat;
   oAdjMat->N = nWaters;

   return oAdjMat;
}

/***************************************************************************/

void DeleteHbonds(struct AdjMat* oAdjMat) {
   assert(oAdjMat != NULL);

   for (unsigned int i = 0; i < oAdjMat->N; i++) {
      delete [] oAdjMat->ppiAdjMat[i];
   }
   delete [] oAdjMat->ppiAdjMat;
   delete oAdjMat;
}

/***************************************************************************/

int TotalHbonds(const struct AdjMat* oAdjMat) {
   assert(oAdjMat != NULL);

   int total = 0;
   for (unsigned int i = 0; i < oAdjMat->N; i++) {
      for (unsigned int j = 0; j < oAdjMat->N; j++) {
	 total += oAdjMat->ppiAdjMat[i][j];
      }
   }

   return total/2;
}

/***************************************************************************/

int PairBonded(const struct AdjMat* oAdjMat,unsigned int i,unsigned int j) {
   assert(oAdjMat != NULL);
   if (i >= oAdjMat->N || j >= oAdjMat->N) {
      return 0;
   }
   return oAdjMat->ppiAdjMat[i][j];
}

/***************************************************************************/

std::vector<int> SingleHbonds(const struct AdjMat* oAdjMat, unsigned int index) {
   assert(oAdjMat != NULL);

   std::vector<int> vHbonds;
   if (index >= oAdjMat->N) {
      return vHbonds;
   }

   for (unsigned int i = 0; i < oAdjMat->N; i++) {
      if( oAdjMat->ppiAdjMat[index][i] ) {
	 vHbonds.push_back(i);
      }
   }

   return vHbonds;
}

/***************************************************************************/

void DistributionHbonds(const struct AdjMat* oAdjMat, int *piHbonds) {
   assert(oAdjMat != NULL);

   for (unsigned int i = 0; i < oAdjMat->N; i++) {
      int total = 0;
      for (unsigned int j = 0; j < oAdjMat->N; j++) {
	 total += oAdjMat->ppiAdjMat[i][j];
      }
      piHbonds[total]++;
   }

}

/***************************************************************************/

void PrintAdjMatrix(const struct AdjMat* oAdjMat) {
   assert(oAdjMat != NULL);

   for (unsigned int i = 0; i < oAdjMat->N; i++) {
      for (unsigned int j = 0; j < oAdjMat->N; j++) {
	 printf("%d  ", oAdjMat->ppiAdjMat[i][j]);
      }
      printf("\n");
   }
}

/***************************************************************************/
