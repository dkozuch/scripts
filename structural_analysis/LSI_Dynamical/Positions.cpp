/***************************************************************************
 * Positions.cpp
 * implementation of positions functions
  ***************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <cmath>
#include "Positions.h"

/***************************************************************************/

static void PrintTraj(Traj_T oTraj) {
   for (int i = 0; i < oTraj->iNumFrames; i++) {
      // get passes first two lines
      int *ID_i = (oTraj->pFrames+i)->piType;
      double *X_i = (oTraj->pFrames+i)->pdX;
      double *Y_i = (oTraj->pFrames+i)->pdY;
      double *Z_i = (oTraj->pFrames+i)->pdZ;
      //read in coords of a frame
      printf("Frame number: %d\n", i+1);
      for (int j = 0; j < oTraj->iN; j++) {
	 printf("%d %lf %lf %lf\n", ID_i[j], X_i[j], Y_i[j], Z_i[j]);
      }
   }
}

/***************************************************************************/

Traj_T CreateTrajectoryXYZ(const char* pcXYZ, double dens) {
   assert(pcXYZ != NULL);

   FILE *fpXYZ = fopen(pcXYZ, "r");
   if (fpXYZ == NULL) {
      printf("Unable to open file");
      return NULL;
   }

  // make sure data is formatted properly and figure out number of frames
   int iN = 0;
   if (fscanf(fpXYZ, "%d", &iN) != 1) {
      printf("file must begin with the number of particles");
      return NULL;
   }
   const double dGperCCtoNtoCA = 6.02214/180.1528; // converts g/cc to number of waters per cubic angstrom;
   dens *= dGperCCtoNtoCA;
   const double nAtoms = 3.0; // #atoms in a water molecule
   const double L = pow((double)iN/nAtoms/dens, 1.0/3.0);
   printf("Box lenghth: %f\n", L);

   char pCh[1000];
   fgets(pCh, 1000, fpXYZ); // reads just a newline char
   fgets(pCh, 1000, fpXYZ);
   if (pCh[0] != 'A') {
      printf("second line is not correct");
      return NULL;
   }

   int iNumFrames = 1; // already passed the first 'Atoms' in the file
   while(fgets(pCh, 1000, fpXYZ) != NULL) {
     // printf("%s", pCh); 
     if (pCh[0] == 'A') {
	 iNumFrames++;
      }
   }
   fclose(fpXYZ);

   // allocate space for trajectory
   Traj_T oTraj = (Traj_T)malloc(sizeof(struct Trajectory));
   assert(oTraj != NULL); 
   oTraj->iNumFrames = iNumFrames;
   oTraj->iN = iN;

   //oTraj->pFrames = (struct Frame*)malloc(iNumFrames*sizeof(struct Frame)); // for some reason it doesn't like this
   oTraj->pFrames = (struct Frame*)calloc(iNumFrames, sizeof(struct Frame));
   assert(oTraj->pFrames != NULL);
   for (int i = 0; i < iNumFrames; i++) {
      (oTraj->pFrames+i)->piType = (int *)malloc(iN*sizeof(int));
      assert((oTraj->pFrames+i)->piType != NULL);
      (oTraj->pFrames+i)->pdX = (double *)malloc(iN*sizeof(double));
      (oTraj->pFrames+i)->pdY = (double *)malloc(iN*sizeof(double));
      (oTraj->pFrames+i)->pdZ = (double *)malloc(iN*sizeof(double));
      (oTraj->pFrames+i)->iN = iN; 
      assert((oTraj->pFrames+i)->pdX != NULL);
      assert((oTraj->pFrames+i)->pdY != NULL);
      assert((oTraj->pFrames+i)->pdZ != NULL);
   }
 
   // populate each frame
   fpXYZ = fopen(pcXYZ, "r");
   for (int i = 0; i < iNumFrames; i++) {
      // get passes first two lines
      fgets(pCh, 1000, fpXYZ);
      fgets(pCh, 1000, fpXYZ);
      int *ID_i = (oTraj->pFrames+i)->piType;
      double *X_i = (oTraj->pFrames+i)->pdX;
      double *Y_i = (oTraj->pFrames+i)->pdY;
      double *Z_i = (oTraj->pFrames+i)->pdZ;
      for (int j = 0; j < 3; j++) {
	 ((oTraj->pFrames+i)->pdBox)[j] = L;
      }
      //read in coords of a frame
      for (int j = 0; j < iN; j++) {
	 fscanf(fpXYZ,"%d %lf %lf %lf", ID_i+j, X_i+j, Y_i+j, Z_i+j);
      }
      fgets(pCh, 1000, fpXYZ); // reads just a newline char
   }
   fclose(fpXYZ);

   // print trajecory to STDOUT - used for debugging
   //PrintTraj(oTraj);

   return oTraj;
}

/***************************************************************************/

Traj_T CreateTrajectoryGRO(const char* pcXYZ, int vel_flag) {
   assert(pcXYZ != NULL);

   FILE *fpXYZ = fopen(pcXYZ, "r");
   if (fpXYZ == NULL) {
      printf("Unable to open file");
      return NULL;
   }

  // make sure data is formatted properly and figure out number of frames
   char pCh[1000];
   fgets(pCh, 1000, fpXYZ);

   int iN = 0;
   if (fscanf(fpXYZ, "%d", &iN) != 1) { // should reads line with number of atoms
      printf("second line of file is not correct\n");
   }
   fgets(pCh, 1000, fpXYZ); // reads just a newline char
 
   int iLines = 2; // already read 2 lines    
   while(fgets(pCh, 1000, fpXYZ) != NULL) {
      iLines++;
   }
   fclose(fpXYZ);
   int iNumFrames = iLines/(iN+3); // Gro files have 3 lines in addtion to lines with atom info

   // allocate space for trajectory
   Traj_T oTraj = (Traj_T)malloc(sizeof(struct Trajectory));
   assert(oTraj != NULL); 
   oTraj->iNumFrames = iNumFrames;
   oTraj->iN = iN;
   oTraj->pFrames = (struct Frame*)malloc(iNumFrames*sizeof(struct Frame));
   assert(oTraj->pFrames != NULL);
   for (int i = 0; i < iNumFrames; i++) {
      (oTraj->pFrames+i)->piType = (int *)malloc(iN*sizeof(int));
      assert((oTraj->pFrames+i)->piType != NULL);
      (oTraj->pFrames+i)->piMolecule = (int *)malloc(iN*sizeof(int));
      assert((oTraj->pFrames+i)->piMolecule != NULL);
      (oTraj->pFrames+i)->pdX = (double *)malloc(iN*sizeof(double));
      (oTraj->pFrames+i)->pdY = (double *)malloc(iN*sizeof(double));
      (oTraj->pFrames+i)->pdZ = (double *)malloc(iN*sizeof(double));
      (oTraj->pFrames+i)->iN = iN; 
      assert((oTraj->pFrames+i)->pdX != NULL);
      assert((oTraj->pFrames+i)->pdY != NULL);
      assert((oTraj->pFrames+i)->pdZ != NULL);
   }

   // populate each frame
   fpXYZ = fopen(pcXYZ, "r");
   for (int i = 0; i < iNumFrames; i++) {
     
      // get passed first 2 lines
      for (int k = 0; k < 2; k++) {
	 fgets(pCh, 1000, fpXYZ);
      }
     
      // populate XYZ coordinates
      int *ID_i = (oTraj->pFrames+i)->piType;
      int *Mol_i = (oTraj->pFrames+i)->piMolecule;
      double *X_i = (oTraj->pFrames+i)->pdX;
      double *Y_i = (oTraj->pFrames+i)->pdY;
      double *Z_i = (oTraj->pFrames+i)->pdZ;
      //read in coords of a frame
      for (int j = 0; j < iN; j++) {
	 char pcMol[100];
	 char pcType[20];
	 int dum;
	 if (j < 9999) { // stupid gromacs stuff
	    if (vel_flag) {
	       double v0,v1,v2;
	       fscanf(fpXYZ,"%s %s %d %lf %lf %lf %lf %lf %lf", pcMol, pcType, &dum, X_i+j, Y_i+j, Z_i+j, &v0,&v1,&v2);
	    }
	    else {
	       fscanf(fpXYZ,"%s %s %d %lf %lf %lf", pcMol, pcType, &dum, X_i+j, Y_i+j, Z_i+j);
	    }
	 }
	 else {
	    if (vel_flag) {
	       double v0,v1,v2;
	       fscanf(fpXYZ,"%s %s %lf %lf %lf %lf %lf %lf", pcMol, pcType, X_i+j, Y_i+j, Z_i+j, &v0,&v1,&v2);
	    }
	    else {
	       fscanf(fpXYZ,"%s %s %lf %lf %lf", pcMol, pcType, X_i+j, Y_i+j, Z_i+j);
	    }
	 }

         // convert nm to Angstrom;
	 double conv = 10.0;
	 X_i[j] *= conv; Y_i[j] *= conv; Z_i[j] *= conv;
         // extract mol from string
	 char list[] = {'0','1','2','3','4','5','6','7','8','9'};
	 dum = 0;
	 while (pcMol[dum] != '\0') {
	    int notNum = 1;
	    for (int kk = 0; kk < 10; kk++) {
	       if (pcMol[dum] == list[kk]) {
		  notNum = 0;
	       }
	    }
	    if (notNum) {
	       break;
	    }
	    dum++;
	 }
	 if (dum == 0) {
	    printf("issue reading molecule type\n");
	    return NULL;
	 }
	 else {
	    pcMol[dum+1] = '\0';
	 }
	 Mol_i[j] = atoi(pcMol);
         // get id from string
	 const char pcW[]  = "OW";
	 const char pcH1[] = "HW1";
	 const char pcH2[] = "HW2";
	 const char pcM[]  = "MW";
	 const char pcI[]  = "IW4";

	 if (strncmp(pcW,pcType,strlen(pcW)) == 0) {
	    ID_i[j] = 2;
	 }
	 else if (strncmp(pcH1,pcType,strlen(pcH1)) == 0) {
	    ID_i[j] = 1;
	 }
	 else if (strncmp(pcH2,pcType,strlen(pcH2)) == 0) {
	    ID_i[j] = 1;
	 }
	 else if ( strncmp(pcM,pcType,strlen(pcM)) == 0 || strncmp(pcI,pcType,strlen(pcI)) == 0 ) {
	    ID_i[j] = 3;
	 }
	 else {
	    printf("issue reading atom type: %s\n", pcType);
	    return NULL;
	 }
      }
      fgets(pCh, 1000, fpXYZ); // reads just a newline char

      // read box bounds
      double *pdBox = (oTraj->pFrames+i)->pdBox;
      if (fscanf(fpXYZ,"%lf %lf %lf", pdBox, pdBox+1, pdBox+2) != 3) {
	 printf("failed to read box info\n");
	 return NULL;
      }
      for (int x = 0; x < 3; x++) {
	 pdBox[x] *= 10.0; // Angstrom
      }

      fgets(pCh, 1000, fpXYZ); // reads just a newline char
   }
   fclose(fpXYZ);

   // print trajecory to STDOUT - used for debugging
   //PrintTraj(oTraj);

   return oTraj;
}

/***************************************************************************/

Traj_T CreateTrajectoryG96(const char* pcXYZ, int vel_flag) {
   assert(pcXYZ != NULL);

   FILE *fpXYZ = fopen(pcXYZ, "r");
   if (fpXYZ == NULL) {
      printf("Unable to open file");
      return NULL;
   }

  // make sure data is formatted properly and figure out number of frames
   char pCh[1000];
   fgets(pCh, 1000, fpXYZ); fgets(pCh, 1000, fpXYZ); fgets(pCh, 1000, fpXYZ); fgets(pCh, 1000, fpXYZ);

   int iN = 0;
   if (fscanf(fpXYZ, "%d", &iN) != 1) { // should reads line with number of atoms
      printf("second line of file is not correct\n");
   }
   fgets(pCh, 1000, fpXYZ); // reads just a newline char
 
   int iLines = 2; // already read 2 lines    
   while(fgets(pCh, 1000, fpXYZ) != NULL) {
      iLines++;
   }
   fclose(fpXYZ);
   int iNumFrames = iLines/(iN+3); // Gro files have 3 lines in addtion to lines with atom info

   // allocate space for trajectory
   Traj_T oTraj = (Traj_T)malloc(sizeof(struct Trajectory));
   assert(oTraj != NULL); 
   oTraj->iNumFrames = iNumFrames;
   oTraj->iN = iN;
   oTraj->pFrames = (struct Frame*)malloc(iNumFrames*sizeof(struct Frame));
   assert(oTraj->pFrames != NULL);
   for (int i = 0; i < iNumFrames; i++) {
      (oTraj->pFrames+i)->piType = (int *)malloc(iN*sizeof(int));
      assert((oTraj->pFrames+i)->piType != NULL);
      (oTraj->pFrames+i)->piMolecule = (int *)malloc(iN*sizeof(int));
      assert((oTraj->pFrames+i)->piMolecule != NULL);
      (oTraj->pFrames+i)->pdX = (double *)malloc(iN*sizeof(double));
      (oTraj->pFrames+i)->pdY = (double *)malloc(iN*sizeof(double));
      (oTraj->pFrames+i)->pdZ = (double *)malloc(iN*sizeof(double));
      (oTraj->pFrames+i)->iN = iN; 
      assert((oTraj->pFrames+i)->pdX != NULL);
      assert((oTraj->pFrames+i)->pdY != NULL);
      assert((oTraj->pFrames+i)->pdZ != NULL);
   }

   // populate each frame
   fpXYZ = fopen(pcXYZ, "r");
   for (int i = 0; i < iNumFrames; i++) {
     
      // get passed first 2 lines
      for (int k = 0; k < 2; k++) {
	 fgets(pCh, 1000, fpXYZ);
      }
     
      // populate XYZ coordinates
      int *ID_i = (oTraj->pFrames+i)->piType;
      int *Mol_i = (oTraj->pFrames+i)->piMolecule;
      double *X_i = (oTraj->pFrames+i)->pdX;
      double *Y_i = (oTraj->pFrames+i)->pdY;
      double *Z_i = (oTraj->pFrames+i)->pdZ;
      //read in coords of a frame
      for (int j = 0; j < iN; j++) {
	 char pcMol[100];
	 char pcType[20];
	 int dum;
	 if (vel_flag) {
	    double v0,v1,v2;
	    fscanf(fpXYZ,"%s %s %d %lf %lf %lf %lf %lf %lf", pcMol, pcType, &dum, X_i+j, Y_i+j, Z_i+j, &v0,&v1,&v2);
	 }
	 else {
	    fscanf(fpXYZ,"%s %s %d %lf %lf %lf", pcMol, pcType, &dum, X_i+j, Y_i+j, Z_i+j);
	 }
         // convert nm to Angstrom;
	 double conv = 10.0;
	 X_i[j] *= conv; Y_i[j] *= conv; Z_i[j] *= conv;
         // extract mol from string
	 char list[] = {'0','1','2','3','4','5','6','7','8','9'};
	 dum = 0;
	 while (pcMol[dum] != '\0') {
	    int notNum = 1;
	    for (int kk = 0; kk < 10; kk++) {
	       if (pcMol[dum] == list[kk]) {
		  notNum = 0;
	       }
	    }
	    if (notNum) {
	       break;
	    }
	    dum++;
	 }
	 if (dum == 0) {
	    printf("issue reading molecule type\n");
	    return NULL;
	 }
	 else {
	    pcMol[dum+1] = '\0';
	 }
	 Mol_i[j] = atoi(pcMol);
         // get id from string
	 const char pcW[]  = "OW";
	 const char pcH1[] = "HW2";
	 const char pcH2[] = "HW3";
	 const char pcM[]  = "MW4";
	 if (strcmp(pcW,pcType) == 0) {
	    ID_i[j] = 2;
	 }
	 else if (strcmp(pcH1,pcType) == 0) {
	    ID_i[j] = 1;
	 }
	 else if (strcmp(pcH2,pcType) == 0) {
	    ID_i[j] = 1;
	 }
	 else if (strcmp(pcM,pcType) == 0) {
	    ID_i[j] = 3;
	 }
	 else {
	    printf("issue reading atom type\n");
	    return NULL;
	 }
      }
      fgets(pCh, 1000, fpXYZ); // reads just a newline char

      // read box bounds
      double *pdBox = (oTraj->pFrames+i)->pdBox;
      if (fscanf(fpXYZ,"%lf %lf %lf", pdBox, pdBox+1, pdBox+2) != 3) {
	 printf("failed to read box info\n");
	 return NULL;
      }
      for (int x = 0; x < 3; x++) {
	 pdBox[x] *= 10.0; // Angstrom
      }

      fgets(pCh, 1000, fpXYZ); // reads just a newline char
   }
   fclose(fpXYZ);

   // print trajecory to STDOUT - used for debugging
   //PrintTraj(oTraj);

   return oTraj;
}

/***************************************************************************/

void FreeTrajectory(Traj_T oTraj) {
   assert(oTraj != NULL);

   for (int i = 0; i < oTraj->iNumFrames; i++) {
      free((oTraj->pFrames+i)->piType);
      free((oTraj->pFrames+i)->piMolecule);
      free((oTraj->pFrames+i)->pdX);
      free((oTraj->pFrames+i)->pdY);
      free((oTraj->pFrames+i)->pdZ);
   }

   free(oTraj->pFrames);
   free(oTraj);
}

/***************************************************************************/

// returns number of frames in a trajectory

int NumFrames(Traj_T oTraj) {
   assert(oTraj != NULL);
   return oTraj->iNumFrames;
}

/***************************************************************************/

int CreateDataFile_TIP4P2005(Traj_T oTraj, int iFrame, const char *pcFileName) {
   assert(oTraj != NULL);

   FILE *pfFile = fopen(pcFileName, "w"); 
   if (pfFile == NULL) {
      printf("failed to open %s for writing data\n", pcFileName);
      return 1;
   }

   fprintf(pfFile, "LAMMPS data file TIP4P2005\n");
   fprintf(pfFile, "\n");
   fprintf(pfFile, "\n");
   fprintf(pfFile, "# atom number --> identity\n");
   fprintf(pfFile, "# 1 --> hydrogen\n");
   fprintf(pfFile, "# 2 --> oxygen\n");
   fprintf(pfFile, "\n");
   fprintf(pfFile, "\n");

   if (iFrame >= oTraj->iNumFrames) {
      printf("frame requested exceeds number of frames in trajectory\n");
      printf("max frame = %d\n",oTraj->iNumFrames-1);
      return 1; 
   }
   const Frame_T pThisFrame = oTraj->pFrames+iFrame;

   /* some overall system specs */
   int iNumWaters = (pThisFrame->iN)/4; // very specific to problem at hand
   int iAtoms = 3*iNumWaters;
   int iBonds = 2*iNumWaters;
   int iAngles = iNumWaters;
   int iAtomTypes = 2; /* distinguish plates with dif type */
   int iBondTypes = 1;
   int iAngleTypes = 1;

   fprintf(pfFile, "%12d  atoms\n", iAtoms);
   fprintf(pfFile, "%12d  bonds\n", iBonds);
   fprintf(pfFile, "%12d  angles\n", iAngles);
   fprintf(pfFile, "%12d  atom types\n", iAtomTypes);
   fprintf(pfFile, "%12d  bond types\n", iBondTypes);
   fprintf(pfFile, "%12d  angle types\n", iAngleTypes);
   fprintf(pfFile, "\n");
   fprintf(pfFile, "\n");

   /* box dimensions */
   fprintf(pfFile, "0.0000000 %15.10f   xlo xhi\n", pThisFrame->pdBox[0]);
   fprintf(pfFile, "0.0000000 %15.10f   ylo yhi\n", pThisFrame->pdBox[1]);
   fprintf(pfFile, "0.0000000 %15.10f   zlo zhi\n", pThisFrame->pdBox[2]);
   fprintf(pfFile, "\n");
   fprintf(pfFile, "\n");

/* specify each atom and corresponding info */
   fprintf(pfFile, "Atoms\n");
   fprintf(pfFile, "# atom_id, molecule_id, atom_type, q, x, y, z\n");
   int iAtomId = 1;
/* write in water info */
   iAtomId = 1;
   for (int i = 0; i < pThisFrame->iN; i++) {
      int iMolId = pThisFrame->piMolecule[i];
      if (pThisFrame->piType[i] == 2) {
	 fprintf(pfFile, "%5d  %4d  %3d  %7.4f  %9.6f  %9.6f  %9.6f\n",
		 iAtomId, iMolId, 2, -1.1128, pThisFrame->pdX[i], pThisFrame->pdY[i], pThisFrame->pdZ[i]);
	 iAtomId++;
      }
      else if (pThisFrame->piType[i] == 1) {
	 fprintf(pfFile, "%5d  %4d  %3d  %7.4f  %9.6f  %9.6f  %9.6f\n",
		 iAtomId, iMolId, 1, 0.5564, pThisFrame->pdX[i], pThisFrame->pdY[i], pThisFrame->pdZ[i]);
	 iAtomId++;
      }
   }
   fprintf(pfFile, "\n");
   fprintf(pfFile, "\n");

/* Write in masses */
   const double dMasses[2] = {1.00794, 15.9994};
   fprintf(pfFile, "Masses\n");
   fprintf(pfFile, "# atom_type, mass\n");
   fprintf(pfFile, "%11d   %9.6f\n", 1, dMasses[0]);
   fprintf(pfFile, "%11d   %9.6f\n", 2, dMasses[1]);
   fprintf(pfFile, "\n");
   fprintf(pfFile, "\n");

/* Write Bond Coeffs */
   fprintf(pfFile, "Bond Coeffs\n");
   fprintf(pfFile, "\n");
   fprintf(pfFile, "1  2000.0  0.9572\n");
   fprintf(pfFile, "\n");
   fprintf(pfFile, "\n");

/* Write Bonds */
   fprintf(pfFile, "Bonds\n");
   fprintf(pfFile, "\n");
   int iCount = 1;
   /* Bonds in TIP4P Water */
   for (int i = 1; i <= iAtoms; i+=3) {
      fprintf(pfFile, "%8d   1 %6d %6d\n", iCount, i, i+1);
      iCount++;
      fprintf(pfFile, "%8d   1 %6d %6d\n", iCount, i, i+2);
      iCount++;
   }
   fprintf(pfFile, "\n");

/* Write angle Coeffs */
   fprintf(pfFile, "Angle Coeffs\n");
   fprintf(pfFile, "\n");
   fprintf(pfFile, "1  450  104.52\n"); /* unique to TIP4P/2005 */
   fprintf(pfFile, "\n");
   fprintf(pfFile, "\n");

   /* Write Angles */
   fprintf(pfFile, "Angles\n");
   fprintf(pfFile, "\n");
   for (int i = 0; i < iNumWaters; i++) {
      int j = 3*i+1;
      fprintf(pfFile,"%8d   1  %5d %5d %5d\n",i+1,j+1,j,j+2);
   }
   fprintf(pfFile, "\n");
   fprintf(pfFile, "\n");

   fclose(pfFile);

   return 0;
}

