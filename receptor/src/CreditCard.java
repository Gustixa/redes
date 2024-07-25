public class CreditCard {
    private long cardNumber;

    public CreditCard(long cardNumber){
        this.cardNumber = cardNumber;
    }
    
    /**
     * Calcula si esta tarjeta de credito posee un numero valido
     *
     * @return true si el numero es valido, false si no.
     */
    public boolean isValid() {

        /**
         * PseudoCode for isValid:
         * sum = 0
         * count = 0
         * for each digit starting from the right
         *      count ++
         *      if count is odd
         *          sum = sum + digit
         *      else if (digit < 5)
         *          sum = sum + 2 * digit
         *      else
         *          sum = sum + 2 * digit - 9
         *  if the last digit of the sum is zero
         *      The card number is valid
         */ 

         long n = (int)cardNumber;
         int sum = 0;
         int count = 0;

         // TODO this is the code from the last question. you can use it
         // as a starting point, but you will need to change most of it.
         while (n > 0){
            int digit = (int)n % 10;
            if(count % 2 == 1){
                sum += digit;
            } else if (digit < 5){
                sum = sum + 2 * digit;
            } else {
                sum = sum + 2 * digit - 9;
            }
            sum = sum + digit;
            n = n/10;
         }
         return sum % 10 == 0;
    }
}
