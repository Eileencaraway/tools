/********************************
begin:  2017.04.12
copyright: nie pin
email: turelong@gmail.com
this file is used to calculate MSD from dumpfiles

**********************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <iostream>
#include <stdlib.h>
#include <cmath>
#include <fstream>

using namespace std;
int const Nmax_bacteria=10000;

class Bacteria{
public:
  double R[7][2][1000]; // 1000 is for the times
  int state;
  int time_start;
  int time_end;
  void reset(){for(int i = 0; i < 7; i++) for(int k = 0; k < 2; k++) for(int q = 0; q < 1000; q++) R[i][k][q] = 0; time_start = -1; time_end = -1;}
}Bacterium[Nmax_bacteria];

int prepare(int t);
int calculate(int max_bacteria, int time_start);

int main(){
  //set the initial values, create arrays
  char buffer[100];
  char buffer1[100];
  char buffer2[100];
  int count=0;
  int natoms;
  int max_natoms;
  int max_bacteria=0;

  FILE* in;
  for(int i=0;i<Nmax_bacteria;i++){
      Bacterium[i].state = -1;
  }
  //read files
for(int j=0;j<17;j++){
    for(int i = 0; i < Nmax_bacteria; i++) Bacterium[i].reset();
    count=0;
    sprintf(buffer,"ls ../b1_%d/dump* > name_plot.txt",j);system(buffer);
    FILE* in_name = fopen("name_plot.txt","r");
    while(fscanf(in_name,"%s",buffer)>0){ // fscanf is used to store each line of name_plot.txt into
      // buffer at each time
      //cout<<buffer<<endl;
      sprintf(buffer2,"head -n 4 %s | tail -n 1 > out", buffer);system(buffer2);// extract the line with number of atoms
      in = fopen("out","r");
      fscanf(in,"%d",&natoms);//put the number of atoms into natoms
      fclose(in);
      max_bacteria=max(natoms,max_bacteria);



      sprintf(buffer2,"tail -n %d %s > out",natoms,buffer); system(buffer2);//put the data into buffer each time with one line

      prepare(count);// store data in bacterium class

      count+=1;

    }
    fclose(in_name);
    cout<<"preparation is done"<<endl;
    cout<<"max_bacteria"<<max_bacteria<<endl;
    calculate(max_bacteria,j);
}


  return 0;
}

int prepare(int t){
  float x,y;
  int n,mol;
  FILE* in;
  int NumAtomMol=7;
  in =fopen("out","r");
  while(fscanf(in,"%f %f %d %d",&x,&y,&n,&mol)>0){
    //cout<<x<<" "<<y<<" "<<n<<" "<<mol<<endl;
    Bacterium[n].R[0][0][t]=x;
    Bacterium[n].R[0][1][t]=y;
    Bacterium[n].state=1;
    if(Bacterium[n].time_start == -1) Bacterium[n].time_start = t;
    Bacterium[n].time_end = t;
    for(int i = 1; i < NumAtomMol; i++){
      fscanf(in,"%f %f %d %d",&x, &y,&n, &mol);
      Bacterium[n].R[i][0][t]=x;
      Bacterium[n].R[i][1][t]=y;//suppose this is public
      }
   }
  fclose(in);

  return 0;
}

int calculate (int max_bacteria,int time_start){

  //set the initial values, create arrays
  float L=66;
  int count1=0;
  int sample=1000;
  float dr2,sum,msd;
  cout<<"we come here"<<endl;
  float dx[max_bacteria],dy[max_bacteria];//might be too large
  cout<<"we come here0."<<endl;
  float x[max_bacteria],y[max_bacteria]; //max_bacteria=1358
  cout<<"we come here0"<<endl;
  sum=0;
  char buffer[100];
  cout<<"we come here1"<<endl;
  sprintf(buffer,"MSD_%d.txt", time_start);
  cout<<"we come here2"<<endl;
  ofstream outfile(buffer);
  cout<<"we come here3"<<endl;
  cout<<"calculation started"<<time_start<<endl;
  // this part is only for calculate msd, store the data is above
  for(int i=0;i<max_bacteria;i++){x[i]=0; y[i]=0;}

      for(int t=1;t<sample;t++){
        count1=0;
        sum=0;
        for(int i=0;i<max_bacteria;i++){
        //  if(Bacterium[i].state==1){//means the bacteria exist in this time frame
        //  if((Bacterium[i].time_start<t)&(Bacterium[i].time_end>=t)){
         if(Bacterium[i].time_start==0){
            //cout<<"bacteria+"<<Bacterium[i].R[3][0][t0+t1]<<endl;
            //cout<<"bacteria-"<<Bacterium[i].R[3][0][t0+t1-1]<<endl;
            dx[i]=Bacterium[i].R[3][0][t]-Bacterium[i].R[3][0][t-1];
            dy[i]=Bacterium[i].R[3][1][t]-Bacterium[i].R[3][1][t-1];
            if(abs(dx[i])>L/2){
              if(dx[i]<0){
                dx[i]=L-abs(dx[i]);
              }else{
                dx[i]=abs(dx[i])-L;
              }
            }
            if(abs(dy[i])>L/2){
              if(dy[i]<0){
                dy[i]=L-abs(dy[i]);
              }else{
                dy[i]=abs(dy[i])-L;
              }

            }
            x[i]+=dx[i];// for bacteria i , x[i] store the displacement from its begining to t
            y[i]+=dy[i];
            dr2=x[i]*x[i]+y[i]*y[i];
            sum+=dr2;
            /*
            if(dx[i][t]>0.1 || dy[i][t]>0.1){
              cout<<"time "<<t<<" atomid "<<i<<" dx "<<dx[i][t]<<" dy "<<dy[i][t]<<endl;
            }*/
          // sum over bacteria
            count1+=1;
          }
        }
        //cout<<"time "<<t<<" sum "<<sum<<" count "<<count1<<endl;
        msd=sum/count1;//from t0 to t1+t0, got several msd value
        //all the bacteria exist at the time t, contribute to msd here.
        outfile<<msd<<endl;
      }


/*
    cout<<"atomid"<<6<<" x at 201 "<<Bacterium[6].R[3][0][201]<<" x at 200 "<<Bacterium[6].R[3][0][200]<<" y at 201 "<<Bacterium[6].R[3][1][201]<<" y at 200 "<<Bacterium[6].R[3][1][200]<<endl;
    cout<<"atomid"<<30<<" x at 201 "<<Bacterium[30].R[3][0][201]<<" x at 200 "<<Bacterium[30].R[3][0][200]<<" y at 201 "<<Bacterium[30].R[3][1][201]<<" y at 200 "<<Bacterium[30].R[3][1][200]<<endl;
    cout<<"atomid"<<43<<" x at 201 "<<Bacterium[43].R[3][0][201]<<" x at 200 "<<Bacterium[43].R[3][0][200]<<" y at 201 "<<Bacterium[43].R[3][1][201]<<" y at 200 "<<Bacterium[43].R[3][1][200]<<endl;
    cout<<"atomid"<<62<<" x at 201 "<<Bacterium[62].R[3][0][201]<<" x at 200 "<<Bacterium[62].R[3][0][200]<<" y at 201 "<<Bacterium[62].R[3][1][201]<<" y at 200 "<<Bacterium[62].R[3][1][200]<<endl;
    cout<<"atomid"<<68<<" x at 201 "<<Bacterium[68].R[3][0][201]<<" x at 200 "<<Bacterium[68].R[3][0][200]<<" y at 201 "<<Bacterium[68].R[3][1][201]<<" y at 200 "<<Bacterium[68].R[3][1][200]<<endl;
    cout<<"atomid"<<74<<" x at 201 "<<Bacterium[74].R[3][0][201]<<" x at 200 "<<Bacterium[74].R[3][0][200]<<" y at 201 "<<Bacterium[74].R[3][1][201]<<" y at 200 "<<Bacterium[74].R[3][1][200]<<endl;
    cout<<"atomid"<<247<<" x at 201 "<<Bacterium[247].R[3][0][201]<<" x at 200 "<<Bacterium[247].R[3][0][200]<<" y at 201 "<<Bacterium[247].R[3][1][201]<<" y at 200 "<<Bacterium[247].R[3][1][200]<<endl;
    cout<<"atomid"<<249<<" x at 201 "<<Bacterium[249].R[3][0][201]<<" x at 200 "<<Bacterium[249].R[3][0][200]<<" y at 201 "<<Bacterium[249].R[3][1][201]<<" y at 200 "<<Bacterium[249].R[3][1][200]<<endl;
*/

    outfile.close();
  return 0;
}
