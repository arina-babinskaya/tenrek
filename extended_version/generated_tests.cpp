#include <gtest/gtest.h>
#include "level1.cpp"


TEST(isPrimeTest, Case0) {
    auto result = isPrime(/*stub:long long*/);
    EXPECT_EQ(result, /*?*/);
}

TEST(printStatsTest, Case0) {
printStats(0, /*stub:float **/, /*stub:double **/, /*stub:float **/, /*stub:float **/);
    SUCCEED();
}

TEST(printStatsTest, Case1) {
printStats(1, /*stub:float **/, /*stub:double **/, /*stub:float **/, /*stub:float **/);
    SUCCEED();
}

TEST(printStatsTest, Case2) {
printStats(-1, /*stub:float **/, /*stub:double **/, /*stub:float **/, /*stub:float **/);
    SUCCEED();
}


#ifndef HAS_CUSTOM_MAIN
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
#endif
