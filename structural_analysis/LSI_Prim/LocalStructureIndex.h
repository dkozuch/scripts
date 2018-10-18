/***************************************************************************
 * LocalStructureIndex.h
 ***************************************************************************/

#ifndef LocalStructureIndex_INCLUDED
#define LocalStructureIndex_INCLUDED

#include "FindHbonds.h"

class LocalStructureIndex {
  public:
   LocalStructureIndex(const struct WaterSystem* oWaterSys, const double dCut, const double dLSI_cut);
   ~LocalStructureIndex();

   std::vector<double> LSI();
   void LSI(const double dCut);

  private:
   int CreateNeighborList();

   const struct WaterSystem* m_oWaterSys;
   const double m_dRooCut_2;
   const double m_dLSI_cut;
   const int m_min_neigh;

   std::vector<std::vector<int> >     m_vvNeighList;
   std::vector<std::vector<double> >  m_vvRij_2;
   std::vector<std::vector<double> >  m_vvRij;
};

#endif //LocalStructureIndex_INCLUDED
