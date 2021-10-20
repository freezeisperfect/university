#include <iostream>
#include <unistd.h>
#include <time.h>
#include <list>
#include <fstream>
using namespace std;
#define R1 6
#define G1 9
#define B1 11

double uniform(double min, double max)
{
    return ((double)rand()/RAND_MAX)*(max - min) + min;
}

class Cashier {
  private:
    int qnum;
    double min;
    double max;
  public:
    Cashier(double a, double b, int c) {qnum = c; min = a; max = b;};
    void Checking(double, double, ofstream&);
    void Job();
    list<int> q;
    list<int> enter;
    list<double> enterTime;      //время входа в обработку
    list<double> jobTime;        //время выхода из обработки
};

void Cashier::Checking(double t, double arr_t, ofstream& f) {
  if (!enterTime.empty()) {
    for (auto i = enterTime.begin() ; i!=enterTime.end();) {
      auto iter = enter.begin();
      if (arr_t - *i > 0) {
        f << "В момент времени " << enterTime.front() << " транзакт " << enter.front() << " встал на выполнение\n";
        i = enterTime.erase(i);
        iter = enter.erase(iter);
      }
      else {
        ++i;
        ++iter;
      }
    }

  }

  if (!jobTime.empty()) {
      for (auto i = jobTime.begin() ; i!=jobTime.end(); ) {
        auto iter = q.begin();
        if (arr_t - *i > 0) {
          //      cout << arr_t - *i << endl;
          f << "В момент времени " << jobTime.front() << " транзакт " << q.front() << " вышел из обработки\n";
          i = jobTime.erase(i);
          iter = q.erase(iter);
          //iter++;
        }
        else {
          ++i;
          ++iter;
        }
      }

  }


}

void Cashier::Job() {
  double worktime = uniform (min, max);
  if (q.size() > 0) {
    jobTime.push_back(enterTime.back() + worktime);
  }
  else {
    jobTime.push_back(enterTime.front() + worktime);
  }
}

int main () {
  srand((unsigned int)time(0));
  int counter = 0;
  double arrival_time = 0;
  ofstream fout;
  fout.open("log2.txt", ios::trunc);

  Cashier q1 (R1, R1 + G1 + B1, 1);
  Cashier q2 (G1, R1 + G1 + B1, 2);

  while (arrival_time < 3600) {
    double time = uniform(0, R1 + G1 + B1);
    arrival_time += time;
    counter++;
    q1.Checking(time, arrival_time, fout);
    q2.Checking(time, arrival_time, fout);

    if (q2.q.size() < q1.q.size()) {
      fout << "В момент времени " << arrival_time << " транзакт " << counter << " встал в очередь 2\n";
      q2.q.push_back(counter);
      if (q2.enterTime.empty()) {
        q2.enterTime.push_back(arrival_time);
        q2.enter.push_back(counter);
      }
      else {
        q2.enterTime.push_back(q2.jobTime.back());
        q2.enter.push_back(counter);
      }
      q2.Job();
    }
    else {
      fout << "В момент времени " << arrival_time << " транзакт " << counter << " встал в очередь 1\n";
      q1.q.push_back(counter);
      if (q1.enterTime.empty()) {
        q1.enterTime.push_back(arrival_time);
        q1.enter.push_back(counter);
      }
      else {
        q1.enterTime.push_back(q1.jobTime.back());
        q1.enter.push_back(counter);
      }
      q1.Job();
    }
  }
  
  fout.close();
  return 0;
}
