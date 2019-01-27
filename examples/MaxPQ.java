/*
MaxPQ interface
Submitted by Andrew Greenwell, Austin St. Onge
*/
public interface MaxPQ<Key extends Comparable<Key>> {
  Key delMax();
  void insert(Key key);
  boolean isEmpty();
  int size();
  String toString();
}

