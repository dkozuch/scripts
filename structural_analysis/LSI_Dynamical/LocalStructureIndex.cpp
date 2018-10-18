/***************************************************************************
 * LocalStructureIndex.cpp
 ***************************************************************************/
#include <cstdio>
#include <cmath>
#include <vector>
#include <cassert>

#include "LocalStructureIndex.h"
#include "FindHbonds.h"

/***************************************************************************/

LocalStructureIndex::LocalStructureIndex(const struct WaterSystem* oWaterSys, const double dCut, const double dLSI_cut) :
   m_oWaterSys(oWaterSys), m_dRooCut_2(dCut*dCut), m_dLSI_cut(dLSI_cut), m_min_neigh(4) {

   assert(m_oWaterSys != NULL);
}

/***************************************************************************/

LocalStructureIndex::~LocalStructureIndex() {
}

/***************************************************************************/

std::vector<double> LocalStructureIndex::LSI() {

   const unsigned int iN = m_oWaterSys->N;
   std::vector<double> vLSI(iN,0.0);

   // create neighbor list
   if ( CreateNeighborList() ) {
      return vLSI;
   }

   for (int i = 0; i < iN; i++) {

      int nLSI = 0;
      for (int neigh = 0; neigh < m_vvNeighList[i].size(); neigh++) {
	 if ( m_vvRij[i][neigh] <= m_dLSI_cut ) {
	    nLSI += 1;
	 }
      }

      // compute LSI for a given water
      double dRavg = 0.0;
      double pdR[nLSI];

      for (int k = 0; k < nLSI; k++) {
	 pdR[k] = m_vvRij[i][k+1] - m_vvRij[i][k];
	 dRavg += pdR[k];
      }
      dRavg /= (double)nLSI;

      for (int k = 0; k < nLSI; k++) {
	 vLSI[i] += (pdR[k] - dRavg)*(pdR[k] - dRavg);
      }

      vLSI[i] /= (double)nLSI;
   }
}

/***************************************************************************/
// Private Functions
/***************************************************************************/

int LocalStructureIndex::CreateNeighborList() {

   const unsigned int iN = m_oWaterSys->N;
   const struct Water* oWaters = m_oWaterSys->pH20;
   int piNumNeigh[iN];
   for (int i = 0; i < iN; i++) {
      piNumNeigh[i] = 0;
   }
   std::vector<std::vector<int> >     vvNeighList(iN);
   std::vector<std::vector<double> >  vvRij_2(iN);

   for (int i = 0; i < iN-1; i++) {
      for (int j = i+1; j < iN; j++) {
	 double dXYZ[3];
	 double dRoo_2 = 0.0;
	 for (int n = 0; n < 3; n++) {
	    dXYZ[n] = oWaters[j].pdO[n] - oWaters[i].pdO[n];
	    dXYZ[n] -= m_oWaterSys->pdBox[n]*round(dXYZ[n] / m_oWaterSys->pdBox[n]);;
	    dRoo_2 += dXYZ[n]*dXYZ[n];
	 }
	 if (dRoo_2 <= m_dRooCut_2) {
	    piNumNeigh[i] += 1;
	    piNumNeigh[j] += 1;
	    vvNeighList[i].push_back(j);
	    vvNeighList[j].push_back(i);

	    vvRij_2[i].push_back(dRoo_2);
	    vvRij_2[j].push_back(dRoo_2);
	 }
      }

      if (piNumNeigh[i] < m_min_neigh) {
	 return 1;
      }
   }

   for (int i = 0; i < iN; i++) {

      std::vector<int>    vNeigh = vvNeighList[i];
      std::vector<double> vRij_2 = vvRij_2[i];

      std::vector<int> vList(vNeigh.size(),0);
      std::vector<double> vR(vNeigh.size(),0);

      double dRmin = 0; 
      for (int num = 0; num < vNeigh.size(); num++) {
	 double dRnext = m_dRooCut_2;
	 for (int neigh = 0; neigh < vNeigh.size(); neigh++) {
	    if ( vRij_2[neigh] > dRmin && vRij_2[neigh] < dRnext ) {
	       dRnext = vRij_2[neigh];
	       vList[num] = vNeigh[neigh];
	    }
	 }
	 vR[num] = dRnext;
	 dRmin = dRnext;
      }
      vvNeighList[i] = vList;
      vvRij_2[i] = vR;
   }

   m_vvNeighList = vvNeighList;
   m_vvRij_2 = vvRij_2;

   std::vector<std::vector<double> >  vvRij(iN);
   for (int i = 0; i < vvRij_2.size(); i++) {
      for (int j = 0; j < vvRij_2[i].size(); j++) {
	 vvRij[i].push_back(sqrt(vvRij_2[i][j]));
      }
   }
   m_vvRij = vvRij;

   return 0;
}

/***************************************************************************/
