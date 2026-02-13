#!/bin/bash

while :; do
  echo "--------------------------------"
  echo "♻️  에이전트 재시작 중..."
  cat PROMPT.md | gemini --yolo
  sleep 0.5
done
