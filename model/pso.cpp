#include <cstdio>
#include <initializer_list>
#include <vector>
#include <iostream>
#include <algorithm>
#include <cstdlib>
#include <random>
#include <functional>
#include <cstring>
#include <string>
#include <limits>

using namespace std;

#define inf() numeric_limits<double>::infinity() 

template<int dim>
struct vec{
    array<double, dim> data;
    vec(){memset(&data,0,sizeof(data));}
    vec(initializer_list<double> inl){
        int i = 0;
        for(auto &v : inl)
            data[i++] = v;
    }
    double& operator[](const int& index){ return data[index];}
    const double& operator[](const int& index) const { return data[index];}
    vec& operator=(const vec& other){if(this!=&other){memcpy(&data,&(other.data),sizeof(data));}return *this;}                                                                           
    friend vec operator+(const vec& lhs, const vec& rhs){vec ret;for (int i=0;i<dim;i++)ret[i]=lhs[i]+rhs[i];return ret;}
    friend vec operator-(const vec& lhs, const vec& rhs){vec ret;for (int i=0;i<dim;i++)ret[i]=lhs[i]-rhs[i];return ret;}
    friend vec operator*(const double& lhs, const vec& rhs){vec ret;for (int i=0;i<dim;i++)ret[i]=lhs*rhs[i];return ret;}
    friend vec operator*(const vec& lhs, const double& rhs){vec ret;for (int i=0;i<dim;i++)ret[i]=lhs[i]*rhs;return ret;}
      
    double len(){
        double ret = 0;
        for(int i=0;i<dim;i++) ret+=data[i]*data[i];
        return sqrt(ret);
    }

    bool up_bound(const vec& upb){
        bool flg = false;
        for(int i=0;i<dim;i++){
            if(upb[i]<data[i]){flg=true;data[i]=upb[i];}
        }
        return flg;
    }
    bool dn_bound(const vec& upb){
        bool flg = false;
        for(int i=0;i<dim;i++){
            if(upb[i]>data[i]){flg=true;data[i]=upb[i];}
        }
        return flg;
    }

    string prt(){
        string s = "[";
        for(int i=0;i<dim-1;i++){s+=to_string(data[i])+", ";}
        s += to_string(data[dim-1]) + "]";return s;
    }

};


template <int dim>
class ParticleGroup{

    public:

    typedef vec<dim> vec;

    struct Particle{
        vec pos;
        vec velocity;
        vec bestpos;
        double fitness;
        double bestfitness;

    };

    //数据
    vector<Particle> pars;
    vec up_bound_pos;
    vec dn_bound_pos;

    //参数
    int n,stepnum;
    double intertia, c1, c2, steprange;

    function<double(const vec&)> targetFunc;

    //运行参量
    double bestfitness;//群体历史最优适应
    vec bestpos;//群体最优位置
    int stepcount = 0;

    //随机数
    std::mt19937 random_generator;
    std::uniform_real_distribution<double> distri;

    // 问题规模，迭代次数，惯性权重，学习因子1、2，迭代步长范围，误差函数
    ParticleGroup(int scale, int stepnum, 
                double intertia, double learnrate_1, 
                double learnrate_2, double steprange,
                function<double(const vec&)> target):
            n(scale), stepnum(stepnum+1), intertia(intertia), 
            c1(learnrate_1), c2(learnrate_2),
            steprange(steprange), targetFunc(target),
            random_generator(42), distri(0.0,1.0){

            for(int i=0;i<scale;i++) pars.emplace_back();
            bestfitness = inf();
            for(int i=0;i<dim;i++) up_bound_pos[i] = inf();
            for(int i=0;i<dim;i++) dn_bound_pos[i] = -inf();

    }

    void Init(vec up_bound_p, vec dn_bound_p, 
        vec up_bound_v, vec dn_bound_v){

        up_bound_pos = up_bound_p;
        dn_bound_pos = dn_bound_p;

        for(auto& v : pars){
            for(int i=0;i<dim;i++){
                double r1 = distri(random_generator);
                double r2 = distri(random_generator);
                v.pos[i] = dn_bound_pos[i] + 
                        r1 * (up_bound_pos[i] - dn_bound_pos[i]);
                v.velocity[i] = dn_bound_v[i] + 
                        r2 * (up_bound_v[i] - dn_bound_v[i]);
            }
            //printf("%s\n", v.pos.prt().c_str());

            //更新群/个体最优值
            double cur = targetFunc(v.pos);
            if(cur <= bestfitness){
                bestfitness = cur;
                bestpos = v.pos;
            }
            v.bestfitness = cur;
            v.bestpos = v.pos;
        }

    }

    bool Iterator(){

        stepcount++;
        if(stepcount >= stepnum) return false;

        
        for(auto& v : pars){
            vec velo;
            double r1 = distri(random_generator);
            double r2 = distri(random_generator);
            velo = velo + intertia * v.velocity;
            velo = velo + c1*r1*(v.bestpos-v.pos);
            velo = velo + c2*r2*(bestpos-v.pos);

            double velo_m = velo.len();
            if(velo_m > steprange){
                velo = velo * steprange;
                velo = velo * (1/velo_m);
            }

            v.pos = v.pos + velo;
            v.velocity = velo;

            //限制位置
            v.pos.up_bound(up_bound_pos);
            v.pos.dn_bound(dn_bound_pos);

            //更新最优位置
            double cur = targetFunc(v.pos);

            if(cur <= bestfitness){
                bestfitness = cur;
                bestpos = v.pos;
            }
            if(cur <= v.bestfitness){
                v.bestfitness = cur;
                v.bestpos = v.pos;
            }
        }

        printf("[Interator %d] Global best err = %lf\n", stepcount, bestfitness);
        printf("[Interator %d] Global best pos = %s\n", stepcount, bestpos.prt().c_str());

        return true;
        
    }

};

vec<4> listeners[7] = {
        {110.241, 27.204, 824, 100.767},
        {110.780, 27.456, 727, 112.220},
        {110.712, 27.785, 742, 188.020},
        {110.251, 27.825, 850, 258.985},
        {110.524, 27.617, 786, 118.443},
        {110.467, 27.921, 678, 266.871},
        {110.047, 27.121, 575, 163.024}
    };

vec<4> multiplier = {97.304, 111.263, 0.001, 0.34};

double err(const vec<4>& v){
    double ret[7] = {0,0,0,0,0,0,0};
    for(int i=0;i<7;i++){
        for(int j=0;j<3;j++){
            int x = listeners[i][j] - v[j];
            ret[i] += x*x;
        }
        ret[i] = abs(sqrt(ret[i]) - (listeners[i][3]-v[3]));
    }
    double rett = 0;
    for(int i=0;i<7;i++){
        rett += ret[i]*ret[i];
    }
    return (rett);
}
double err2(const vec<4>& v){
    double ret[7] = {0,0,0,0,0,0,0};
    for(int i=0;i<7;i++){
        for(int j=0;j<3;j++){
            int x = listeners[i][j] - v[j];
            ret[i] += x*x;
        }
        ret[i] = abs(sqrt(ret[i]) - (listeners[i][3]-v[3]));
        printf("第[%d]个监测站误差为%lf\n", i,ret[i]);
    }
    double rett = 0;
    for(int i=0;i<7;i++){
        rett += ret[i]*ret[i];
    }
    return (rett);
}

double err_test(const vec<4>& v){
    double ret = 0;
    for(int i=0;i<4;i++) ret += (v[i] - 5)*(v[i] - 5);
    ret = sqrt(ret);
    return ret;
}


int main()
{
    for(int i=0;i<7;i++){
        for(int j=0;j<4;j++){
            listeners[i][j] *= multiplier[j];
        }
    }

    ParticleGroup<4> pg(100000,100,0.5,2,2,inf(),err);//0.5, 1.6, 2非常精确

    pg.Init({12000,5000,1,5},{10000,2000,0,-5},{1200,500,0.1,50},{-1200,-500,-0.1,50});

    while(pg.Iterator()){
        ;
    }

    vec<4> bestpos = pg.bestpos;
    //bestpos[3] += 100*multiplier[3];
    printf("[Finished] Global best fitness = %lf\n", err2(bestpos));
    for(int i=0;i<4;i++){
        bestpos[i] /= multiplier[i];
    }

    printf("[Finished] Global best pos = %s\n", bestpos.prt().c_str());

    

    return 0;
}
