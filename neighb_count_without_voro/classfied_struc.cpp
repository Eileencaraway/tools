// informations that this file can provide
//1. in local_density_timestep store the particles id x y z local density number of neighbors at each time
//through 1, I can find out some example those particles in the gas, through eyes
//2. I run this simulation again, to track only those particles I am interest in in a particle_track file
// so that I can get an average
//
//
////////////////////////////////////////////////////////////////
#include <iostream>
#include <fstream>
#include "math.h"
#include <algorithm>
#include <iomanip>
#include <numeric>
#include <vector>
#include <utility>
#include <cstring>
#include <stdio.h>
//#include <string>
//#include <stdlib.h>
//#include "src\voro++.cc"
using namespace std;
//using namespace voro;

//****************************************************************************
// define global variables and const variable
//****************************************************************************
int const N = 10000; //number of particles
int const nfiles = 1000; //I can put larger number then needed?
const double PI = 4*atan(1.0);
double L, HL; //box size and half of the box size
double Rcut = 1.36,Rcut2 = Rcut*Rcut; // cut off of the distance of
double Ncut_gas = 3, Ncut_cluster = 11; //Ncut is determined from experience for classify particles in the gas and liquid(cluster)
int n_x, n_y, n_z; // number of boxes the simulation volume is divided into
double tol = 1E-8;

//****************************************************************************
// class of particles
//****************************************************************************
class particle{
  public:
  double R[3]; // position [x,y,z,xu,yu,zu,omegax,omegay,omegaz,thtx,thty,thtz]
  double q6;
  double Surface_areas;
  double Volume;
  double Nfaces;
  double Radius;
  bool gas_state;
  bool liquid_state;
  bool interm_state;
  int num_neighbors;
  int neighbor[100];
  // constructor, same name as the class, automatically called whenever a new object of this class is created
  // allowing the class to initialize member variables or allocate storage
  particle(){gas_state =1; liquid_state= 1; interm_state=0;}
  void add_neighbor(int m){neighbor[num_neighbors] = m; num_neighbors++;}
  void reset_neighbors(){num_neighbors = 0;}
  void set_VSN(double V, double S, int NF){ Volume = V; Surface_areas = S; Nfaces = NF; }
}Particles[N];

void prepare();
void ReadConf(int &timestep, char* line);//read the configuration file
void determine_neighbors_using_cutoff();
//void determine_neighbors_using_Voronoi();
void determine_state(int &timestep);
void outputdata(double &q6global, int &timestep);
void loop();
double msd();
void outputstate();
void neigh_track();

//****************************************************************************
// main
//****************************************************************************
int main(int argc, char **argv){
    char buffer[100],line[40];
    int step,s_witch,count;
    int timestep;
    double q6global;
    char ch;


	do
	{   cout<<"do 3 steps one by one"<<endl;
        cout<<"1. voronoi "<<endl;
        cout<<"2. trajectory of intermediate state "<<endl;
        cout<<"3. end"<<endl;
        cout<<"please type the number:"<<endl;
	  	ch=getchar();
	  	switch(ch)
	  	{
			case '1':loop();
			   	 break;
		  	case '2':neigh_track();
			    	 break;
		  	case '3':exit(0);
		  	default :cout<<"\a";
		}
    }while(ch!='4');

   return 0;
}

//****************************************************************************
// functions
//****************************************************************************
void loop(){
    int timestep;
    char line[40];
    double q6global;
    prepare();
    ifstream file;
    file.open("files.dat");
    std::string sline;
        int countfile = 0 ;
	while(std::getline(file, sline)){
	  cerr << countfile << endl;
	  countfile++;
	  strcpy(line,sline.c_str());
	  cout <<line<<endl;
	  ReadConf(timestep, line); // change the timestep also
	  //perform the Voronoi tessellation
	  //determine_neighbors_using_Voronoi();
	  determine_neighbors_using_cutoff();
	  determine_state(timestep);
	  //out put information
	  outputdata(q6global,timestep);
	}

	cout<<"finish the voronoi tessellation"<<endl;
    outputstate();
    cout<<"saved the state files"<<endl;
}

void determine_state(int &timestep){
    ofstream  staten;
    char buffer2[100];
    //sprintf(buffer2,"state_%d.dat",timestep);
    staten.open("state.dat",ios::app); // a statistic of number of files
    int ngas=0, nliquid=0;
    for(int n = 0; n < N; n++){
       if (Particles[n].num_neighbors <= 3){
           Particles[n].gas_state =Particles[n].gas_state*1 ;//
           ngas+=1;
       }
       else{
           Particles[n].gas_state = Particles[n].gas_state*0;
       }

       if(Particles[n].num_neighbors>= 11){
           Particles[n].liquid_state =Particles[n].liquid_state*1;
           nliquid+=1;

       }
       else{
          Particles[n].liquid_state = Particles[n].liquid_state*0;
       }

       if((Particles[n].num_neighbors>3)&&(Particles[n].num_neighbors<11)){
           Particles[n].interm_state = 1;
       }
    }
    staten<<timestep<<" "<<ngas<<" "<<nliquid<<endl;
    staten.close();
// in the end, print out a file for the final results of those particle in which state
// do it in the outputdata func
// print out the number of particle in each state at each timestep in a file
}

void prepare(){
    char buffer[100];
    sprintf(buffer,"ls dumpfile.* > files.dat");
    int check=system(buffer);

    sprintf(buffer,"cat dumpfile.0000000000.txt |less|grep 'ITEM: BOX' -A 1|tail -n 1|awk '{print $2}'>> out2");
    check = system(buffer);
    FILE* in2=fopen("out2","r"); // FILE under C
    check = fscanf(in2,"%lf",&L); //define the box size
    HL = L/2;  // give the value again
    // Create a pre-container class to import the input file and guess the best computational grid size to use.
    sprintf(buffer,"cat dumpfile.0000000000.txt |tail -n %d | awk '{print $1,$2,$3,$4,$17}' > cleanfile.txt",N);
    check=system(buffer);
    //pre_container pcon(0, L, 0, L, 0, L,true,true,true);
    //pcon.import("cleanfile.txt");
    //pcon.guess_optimal(n_x,n_y,n_z); // n_x, n_y, n_z is global variables
}

void ReadConf(int &timestep, char* line){
  int i;
  char buffer4[100]; //, line[100];
  sprintf(buffer4,"cat %s |less|grep 'ITEM: TIMESTEP' -A 1|tail -n 1|awk '{print $1}' > tout",line);
  int check=system(buffer4);
  ifstream inFile;
  inFile.open("tout");
  inFile>>timestep;
  //FILE* tin=fopen("tout","r");
  //check = fscanf(tin,"%d",&timestep);
  sprintf(buffer4,"cat %s |tail -n %d | awk '{print $1,$2,$3,$4,$17}' > cleanfile.txt", line,N);
  check=system(buffer4);
  ifstream ConfFile;

  ConfFile.open("cleanfile.txt");
	for(int n = 0; n < N; n++){
	  ConfFile>>i>>Particles[n].R[0] >> Particles[n].R[1] >>Particles[n].R[2]>> Particles[n].Radius;
    }
	ConfFile.close();
}


void outputdata(double &q6global, int &timestep){
  int i;
  char buffer[1000];
   ofstream  local_density;
   sprintf(buffer,"local_density_%d.dat",timestep);
   local_density.open(buffer);
   local_density<<"ITEM: TIMESTEP"<<endl;
   local_density<<timestep<<endl;
   local_density<<"ITEM: NUMBER OF ATOMS" <<endl;
   local_density<<N <<endl;
   local_density<<"ITEM: BOX BOUNDS pp pp pp" <<endl;
   local_density<<"0.0 "<<L<<endl;
   local_density<<"0.0 "<<L<<endl;
   local_density<<"0.0 "<<L<<endl;
   local_density<<"ITEM: ATOMS id x y z radius num_neighbors gas liquid interm" <<endl;
   for(int n = 0; n < N; n++){
	   local_density<<n<<" "<<Particles[n].R[0]<<" "<<Particles[n].R[1]<<" "<<Particles[n].R[2]<<" "<<Particles[n].Radius<<" "<<\
       Particles[n].num_neighbors<<" "<<\
       Particles[n].gas_state<<" "<<Particles[n].liquid_state<<" "<<Particles[n].interm_state<<endl;
	}
   local_density.close();
}

void outputstate(){
    // this is print after the last timestep the id of those states
    int ID;
    ofstream gasfile;
    ofstream clusterfile;
    ofstream intermfile;
    gasfile.open("gas_id.dat");
    clusterfile.open("cluster_id.dat");
    intermfile.open("interm_id.dat");
    for(int n = 0; n < N; n++){
    if(Particles[n].gas_state==1){
        ID = n+1;
        gasfile<<ID<<endl;
    }
    else if(Particles[n].liquid_state==1){
        ID = n+1;
        clusterfile<<ID<<endl;
    }
    else if(Particles[n].interm_state==1){
        ID = n+1;
        intermfile<<ID<<endl;
    }
}
gasfile.close();
clusterfile.close();
intermfile.close();
}
// this is only for the particle in the cluster
/*
double msd(){
    int count3;
    int id;
    ifstream clusterfile;
    clusterfile.open("cluster_id.dat")
    count3 =0;
    while(clusterfile.good()){
        clusterfile>>id;
        count3+=1;
        id_of_cluster.push_back(id);
    }
   //count3 now is the total number of particle in cluster

   ifstream file;
   file.open("files.dat");
   std::string sline;
   while(std::getline(file, sline)){
   strcpy(line,sline.c_str());
   sprintf(buffer,"cat %s |less|grep 'ITEM: TIMESTEP' -A 1|tail -n 1|awk '{print $1}' > tout",line);
   int check = system(buffer);
   FILE* tin=fopen("tout","r");
   check = fscanf(tin,"%d",&timestep);

   ifstream ConfFile;
   ConfFile.open(line);
    for loop over all the row
         if  particle in the cluster
       sum and average // I should use log scale to calculate this
}
*/
void neigh_track(){
    int timestep;
    vector<int> id_of_gas;
    int id,count2;
    double ld;
    char buffer[1000],line[100];
    ifstream jumpfile;
    jumpfile.open("interm_id.dat");
    count2 =0;
    prepare();
    while(jumpfile.good()){
        jumpfile>>id;
        count2+=1;
        id_of_gas.push_back(id);
    }

    ifstream file;
    file.open("files.dat");
    std::string sline;
    ofstream trajfile;
    //sprintf(buffer,"track_nneigh.dat");
    //trajfile.open(buffer);

    while(std::getline(file, sline)){
        strcpy(line,sline.c_str());
        sprintf(buffer,"cat %s |less|grep 'ITEM: TIMESTEP' -A 1|tail -n 1|awk '{print $1}' > tout",line);
        int check = system(buffer);
        FILE* tin=fopen("tout","r");
        check = fscanf(tin,"%d",&timestep);
        ReadConf(timestep, line);
        //cout <<line<<endl;
        determine_neighbors_using_cutoff();

        for(int i=0;i<4000;i++){
            id = id_of_gas[i];
            sprintf(buffer,"track_nneigh_id%d.dat",id);
            trajfile.open(buffer,ios::app);
            trajfile<<timestep<<" "<<Particles[id].num_neighbors<<endl;
            trajfile.close();
        }
    }
}
// details of the functions
/*
void determine_neighbors_using_Voronoi(){
  double x,y,z,r,V,S,NF;
  unsigned int i,j;
  int id;
  voronoicell_neighbor c;  // create an object in voronoicell_neighbor class
  vector<int> neigh,f_vert;
  vector<double> f_area;
  vector<double> v;
  //// open files
  FILE *fp;
  //if (draw) fp=safe_fopen("tessellation.dat", "w");
  container_poly conVoro(0, L,0, L,0, L,n_x,n_y,n_z,true,true,true,8);
  for(int n = 0; n < N; n++){
    x = Particles[n].R[0];
    y = Particles[n].R[1];
	z = Particles[n].R[2];
    r = Particles[n].Radius;
	Particles[n].reset_neighbors();
	conVoro.put(n,x,y,z,r);  // read a particle at a time
  }
  // Loop over all particles in the container and compute each Voronoi cell
  c_loop_all clVoro(conVoro);
  	if(clVoro.start()) do if(conVoro.compute_cell(c,clVoro)) {  //True if the cell was computed. If the cell cannot be computed, if it is removed entirely by a wall or boundary condition, then the routine returns false.
		id=clVoro.pid();
		// Gather information about the computed Voronoi cell
		c.neighbors(neigh);  // return a list of IDs of the neighbor particles
		c.face_areas(f_area);
		S = 0;
		for(i=0;i<neigh.size();i++) {
            S+=f_area[i];  // S contain the total face area
		}
		//=========================
		V = c.volume();
	    NF = neigh.size(); //get number of neighbors i.e number of faces
		Particles[id].set_VSN(V,S,NF);
		//update neighbor information
		 Particles[id].num_neighbors = neigh.size();
		 for(i=0;i<neigh.size();i++) {
			Particles[id].neighbor[i] = neigh[i];  // also record the id of each neigbhors
		}
	} while (clVoro.inc());// True if there is another particle, false if no more particles are available.
  conVoro.clear();
}
*/
//determine the first shell neighbors
void determine_neighbors_using_cutoff(){
	double x,y,z,x1,y1,z1;
	double dr2,dx,dy,dz;
  for(int n = 0; n < N; n++){
	  Particles[n].reset_neighbors();
      x = Particles[n].R[0];
      y = Particles[n].R[1];
	  z = Particles[n].R[2];
	  for(int i = 0; i < N; i++){
		if(i!=n){
		  x1 = Particles[i].R[0];
          y1 = Particles[i].R[1];
	      z1 = Particles[i].R[2];
		  dx = x-x1;
		  dy = y-y1;
		  dz = z-z1;
		  //consider the periodic boundary
		  dx -= L*round(dx/L);
		  dy -= L*round(dy/L);
		  dz -= L*round(dz/L);
		  dr2 = dx*dx + dy*dy + dz*dz;
		  if(dr2<Rcut2) Particles[n].add_neighbor(i);
		}
	  }
  }
}
