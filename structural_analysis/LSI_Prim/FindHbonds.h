/***************************************************************************
 * FindHbonds.h
 ***************************************************************************/

#ifndef FindHbonds_INCLUDED
#define FindHbonds_INCLUDED

#include <vector>

#include "Positions.h"

struct AdjMat {
   unsigned int** ppiAdjMat;
   unsigned int N;
};

struct WaterSystem {
   struct Water* pH20;
   double pdBox[3];
   unsigned int N;
};

struct Water {
   double pdO[3];
   double pdH1[3];
   double pdH2[3];
};

/***************************************************************************/

struct WaterSystem* Frame2Waters(const Frame_T pFrame);

/***************************************************************************/

void DeleteWaters(struct WaterSystem* oWaterSys);

/***************************************************************************/

struct AdjMat* FindHbonds(const struct WaterSystem* oWaterSys);

/***************************************************************************/

void DeleteHbonds(struct AdjMat* oAdjMat);

/***************************************************************************/

int TotalHbonds(const struct AdjMat* oAdjMat);

/***************************************************************************/

int PairBonded(const struct AdjMat* oAdjMat, unsigned int i, unsigned int j);

/***************************************************************************/

std::vector<int> SingleHbonds(const struct AdjMat* oAdjMat, unsigned int i);

/***************************************************************************/

void DistributionHbonds(const struct AdjMat* oAdjMat, int *piHbonds);

/***************************************************************************/

void PrintAdjMatrix(const struct AdjMat* oAdjMat);

/***************************************************************************/

#endif // FindHbonds_INCLUDED
