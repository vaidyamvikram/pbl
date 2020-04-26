import java.io.*; import java.util.*; 
import java.awt.*; 
import java.awt.event.*;
 import javax.swing.*;
 class Display extends JFrame  {  
 public Display()   {   
   GridLayout g = new GridLayout(0, 3);   setLayout(g);   
try   {  
BufferedReader br = new BufferedReader(new FileReader("emp.txt")); 

 String line;                     
while ((line=br.readLine())!= null)           {    
 String datavalue[] = line.split(",");             
  for (int i = 0; i< datavalue.length;i++)   {    
 add(new JLabel(datavalue[i]));   
 }                      } 
 
  } catch (Exception e)   {   
 System.out.println(e);   } 
 setSize(400, 400);   
setVisible(true); 

  setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); 
 
  } 
} 
 
public class Tbl  { 
 public static void main(String[] args)  { 
 Display d = new Display();  
}
 } 