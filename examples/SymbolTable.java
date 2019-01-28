/*
A generic interface for symbol tables.

Written by: Andrew Greenwell
*/

import java.util.*;

public interface SymbolTable<K, V> {

  int getSize();
  void setSize(int N);

  void put(K key, V value);
  V get(K key);
  boolean containsKey(K key);
  Set<K> keySet();

  String toString();

}
