/*
An interface for Max Priority Queues.

Written by: Andrew Greenwell
*/

public interface MaxPQ<Key extends Comparable<Key>> {
  Key delMax();
  void insert(Key key);
  boolean isEmpty();
  int size();
  String toString();
}

