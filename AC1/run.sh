for i in {1..100}; do
sleep 1s &
python3 verifier.py 2 &
python3 prover.py 2;
done
