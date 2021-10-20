#include <iostream>
#include <time.h>
#include <thread>
#include <chrono>
#include <mutex>
#include <queue>
#include <condition_variable>
#include <unistd.h>
#include <fstream>
using namespace std;

#define R1 6
#define G1 9
#define B1 11

double arrival_time = 0 ;

double uniform(double min, double max)
{
    return ((double)rand()/RAND_MAX)*(max - min) + min;
}

class Cashier {
  private:
      double min;
      double max;
			bool status;			// true - свободен, false - занят
      bool dataStatus;
			std::mutex mtx;
			std::condition_variable cv;
  public:
    Cashier(double a, double b) { min = a; max = b; status = true; dataStatus = false;};
		void Job(ofstream&);
    void Waiting();
		queue<int> q;
    queue<double> qtime;
};


void Cashier::Job(ofstream& f){
  bool ifTime = false;
  double t2;
  std::unique_lock <std::mutex> ul (mtx);
	while (arrival_time < 3600) {

		cv.wait(ul, [this]{return dataStatus;});
    if (ifTime == false)
      t2 = qtime.front();
    //printf("В момент времени %.3f транзакт %d встал на выполнение \n", t2, q.front());
    f << "At time " << t2 << " process " << q.front() << " started doing task\n";
    status = false;
		double worktime = uniform(min, max);

    this_thread::sleep_for(std::chrono::duration<double, std::milli>(worktime));
		double endtime = t2 + worktime;
    //printf("В момент времени %.3f транзакт %d обработан \n", endtime, q.front());
    f << "At time " << endtime << " process " << q.front() << " ended doing task\n";
    q.pop();
    qtime.pop();

    if (q.empty() == 0) {t2 = endtime; ifTime = true;} else {ifTime = false;}
    dataStatus = false;
		status = true;
	}
	ul.unlock();
}

void Cashier::Waiting() {
  //std::unique_lock<mutex> lg (mtx);
  while (arrival_time < 3600) {
    if ((q.empty() == false) && (status == true)) {
      dataStatus = true;
      cv.notify_all();
    }
  }
}


int main () {
	srand((unsigned int)time(0));
	int counter = 1;
	Cashier q1(R1, R1 + G1 + B1);
	Cashier q2(G1, R1 + G1 + B1);
  ofstream fout;
  fout.open("log1.txt", ios::trunc);

  thread th1 ([&](){
    q1.Job(fout);
  });
  thread th3 ([&](){
    q1.Waiting();
  });
  thread th2 ([&](){
    q2.Job(fout);
  });
  thread th4 ([&](){
    q2.Waiting();
  });

	while (arrival_time < 3600) {
		double time = uniform (0, R1 + G1 + B1);
		arrival_time += time;
		this_thread::sleep_for(std::chrono::duration<double, std::milli>(time));

		//printf("В момент времени %.3f транзакт %d встал в очередь ", arrival_time, counter);
    fout << "At time " << arrival_time << " process " << counter << " in queue ";
    (q2.q.size() < q1.q.size()) ? fout << "2\n" : fout << "1\n";

    if (q2.q.size() < q1.q.size()) {
			q2.q.push(counter);
      q2.qtime.push(arrival_time);
		}
		else {
			q1.q.push(counter);
      q1.qtime.push(arrival_time);
		}
		counter++;
	}
	th1.join();
	th2.join();
  th3.join();
  th4.join();
  fout.close();
	return 0;
}
