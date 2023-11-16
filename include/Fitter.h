#ifndef __FITTER_H__
#define __FITTER_H__

#include <vector>

class Fitter {
public:
    using Range = std::vector<double>;

    Fitter();
    Fitter(const Range fit_range);
    ~Fitter();

private:
    Range m_fit_range{0, 0};
};

#endif // __FITTER_H__
