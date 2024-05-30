#include <cstdint>
#include <cmath>

extern "C" {
    uint32_t encode_arinc(float value, float min, float max, float scale, uint16_t low_bit, uint16_t label){
    int mask_ = 0x1fffff00;
    uint32_t pack;

    if (value < min) value = min;
    else if (value > max) value = max;

    int32_t ipar = (int)round(abs(value)/scale);

    if (value < 0) ipar = -ipar;

    pack = (ipar << low_bit) & mask_;

    pack = pack|label;

    pack = pack|(0x1 << 29)|(0x1 << 30);

    int count = 0;
    int32_t n = pack;
    while (n) {
        count += n & 1;
        n >>= 1;
    }

    if (count%2 == 0) pack = pack | (1 << 31);

    return pack;
    }
}