
undefined8 main(void)

{
  int iVar1;
  FILE *pFVar2;
  long in_FS_OFFSET;
  int local_44;
  char local_38 [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts(
      "I\'ve implemented a 1-block AES ECB 128 cipher that uses a random key.\nTry to give me a message such as AES_Encrypt(message, key) = 0xdeadbeefdeadbeefcafebabecafebabe.\n(don\'t try too much, this is impossible).\n"
      );
  fflush(stdout);
  pFVar2 = fopen("/dev/urandom","rb");
  fread(key,0x10,1,pFVar2);
  fclose(pFVar2);
  printf("Enter your message: ");
  fflush(stdout);
  fgets(local_38,0x28,stdin);
  sprintf(message,local_38);
  printf("Do you want to change it ? (y/n) ");
  fflush(stdout);
  iVar1 = getc(stdin);
  getc(stdin);
  if ((char)iVar1 == 'y') {
    printf("Enter your message (last chance): ");
    fflush(stdout);
    fgets(local_38,0x28,stdin);
    sprintf(message,local_38);
  }
  printf("So, this is your final message: ");
  local_44 = 0;
  while (local_44 < 0x28) {
    printf("%02x",(ulong)(byte)message[local_44]);
    local_44 = local_44 + 1;
  }
  puts("\n");
  fflush(stdout);
  AES_Encrypt(message,key);
  iVar1 = memcmp(message,expected,0x10);
  if (iVar1 == 0) {
    puts("WHAT ?! THIS IS IMPOSSIBLE !!!");
    pFVar2 = fopen("flag.txt","r");
    while( true ) {
      iVar1 = getc(pFVar2);
      if ((char)iVar1 == -1) break;
      putchar((int)(char)iVar1);
    }
    fflush(stdout);
    fclose(pFVar2);
  }
  else {
    puts("Well, I guess you\'re not this smart :)");
    fflush(stdout);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
