/***************************************************************************
 * Positions.h
 * positions header
  ***************************************************************************/

#ifndef Positions_INCLUDED
#define Positions_INCLUDED

//#include "Positions.h"

typedef struct Trajectory *Traj_T;
typedef struct Frame *Frame_T;

struct Frame {
   int *piType;     // arrary of particle types
   int *piMolecule; // arrary of molecules index of a particle
   double *pdX;     // array of X coords
   double *pdY;     // array of Y coords
   double *pdZ;     // array of Z coords
   int iN;          // number of particles
   double pdBox[3]; // XYZ dimensions of box; origin is at corner of simulation box
};

struct Trajectory {
   int iNumFrames; // number of frames
   Frame *pFrames; // pointer to first frame
   int iN;   // number of particles
};


/***************************************************************************/

// Creates and returns pointer to trajectory object from XYZ file
// need to provide density in g/cc

Traj_T CreateTrajectoryXYZ(const char* pcXYZ, double dens);


/***************************************************************************/

// Creates and returns pointer to trajectory object from GRO file
// vel_flag = 0 means gro does not include velocities
// Postions of atoms are SHIFTED to put origin at the corner of the simulation
// box

Traj_T CreateTrajectoryGRO(const char* pcXYZ, int vel_flag);


/***************************************************************************/

// Creates and returns pointer to trajectory object from g96 file
// vel_flag = 0 means gro does not include velocities
// Postions of atoms are SHIFTED to put origin at the corner of the simulation
// box

Traj_T CreateTrajectoryG96(const char* pcXYZ, int vel_flag);

/***************************************************************************/

void FreeTrajectory(Traj_T oTraj);

/***************************************************************************/

// returns number of frames in a trajectory

int NumFrames(Traj_T oTraj);

/***************************************************************************/

// note that first frame has iFrame = 0;

int CreateDataFile_TIP4P2005(Traj_T oTraj, int iFrame, const char *pcFileName);

/***************************************************************************/

#endif // Positions_INCLUDED
