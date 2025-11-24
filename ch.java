class Solution {
    public int characterReplacement(String s, int k) {
        HashMap<Character, Integer> gmap = new HashMap<>();
        int rep = 0;
        int l = 0;
        int r = 1;
        int max = 1;
        int fmax = 1;
        char smax = s.charAt(0);

        //read right, see the most frequent one, if(l<-->r - frequent > k, move left to right)
        gmap.put(s.charAt(l), 1);
        while(r<s.length()){
            char right = s.charAt(r);
            if(!gmap.containsKey(right)){
                gmap.put(right, 1);
                if((r-l+1) - fmax <= k){
                    rep = (r-l+1) ;
                } else {
                    gmap.put(s.charAt(l), gmap.get(s.charAt(l))-1);
                    l++;
                }
            } else {
                gmap.put(right, gmap.get(right)+1);
                if(gmap.get(right)>fmax){
                    fmax = gmap.get(right);
                    smax = right;
                }
                if((r-l+1) - fmax <= k){
                    rep = (r-l+1);
                } else {
                    gmap.put(s.charAt(l), gmap.get(s.charAt(l)) - 1);
                    l++;
                }
            }

            if((r-l+1) > max) max = (r-l+1);
          
            System.out.println(fmax + " - fmax " + smax + " smax " + rep + " rep" + " range " + l +  "-" + r);
            r++;
        }
        return max;
    }
}
