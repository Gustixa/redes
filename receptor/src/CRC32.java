import java.util.*;

public class CRC32 {

    public String CRC(String dividend, String divisor){
        String str2, div;
        int shift;
        shift = dividend.length() - divisor.length();

        while(shift >= 0){
            dividend = Integer.toBinaryString(Integer.parseInt(dividend,2)^
            (Integer.parseInt(divisor,2)<<shift));
            shift = dividend.length() - divisor.length();
        }

        if (dividend.length() < 16){
            while(dividend.length() != 16){
                dividend = "0"+dividend;
            }
        }
        System.out.println("div" + dividend);
        return dividend;
    }

}
